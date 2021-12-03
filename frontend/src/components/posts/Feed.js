import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { getPosts, deletePost } from "../../actions/posts";
import { addFollower } from "../../actions/followers";
import { CREATE_ALERT, LIKE_POST } from "../../actions/types";

import Moment from "react-moment";
import {
  FaRegClock,
  FaTrashAlt,
  FaWindowClose,
  FaUserAlt,
  FaUserPlus,
  FaRegTrashAlt,
  FaRegEnvelope,
  FaRegThumbsUp,
  FaThumbsUp,
} from "react-icons/fa";

import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import { Redirect } from "react-router-dom";
import { tokenConfig } from "../../actions/auth";
import axios from "axios";
import store from "../../store";

export class Feed extends Component {
  init_state = {
    selectedAuthor: {},
    isFollower: false,
    open: false,
    redirect: "",
  };

  state = this.init_state;

  parseData(data) {
    const parseData = data.id.split("/");
    return parseData[parseData.length - 1];
  }

  componentDidMount() {
    this.props.getPosts();
  }

  onAuthorClick(foreignAuthor) {
    this.setState({
      selectedAuthor: foreignAuthor,
    });

    const auth = this.props.auth;

    const foreignAuthorId = this.parseData(foreignAuthor);

    axios
      .get(
        `/author/${auth.user.author}/followers/${foreignAuthorId}`,
        tokenConfig(store.getState)
      )
      .then((resp) => {
        this.setState({
          isFollower: resp.data.detail,
          open: true,
        });
      });
  }

  handleFollow() {
    if (this.state.isFollower === false) {
      const foreignAuthorId = this.parseData(this.state.selectedAuthor);
      const authorId = this.props.auth.user.author;

      axios
        .put(
          `/author/${foreignAuthorId}/followers/${authorId}`,
          {},
          tokenConfig(store.getState)
        )
        .then((response) => {
          this.setState({
            open: false,
          });
          axios.get(`/author/${authorId}`,
            tokenConfig(store.getState)
          )
          .then((resp) => {
            axios.post(`/author/${foreignAuthorId}/inbox`,
            {
              "type": "follow",      
              "summary":`${resp.data.displayName} wants to follow ${this.state.selectedAuthor.displayName}`,
              "actor":resp.data, //author,
              "object":this.state.selectedAuthor  //foreignAuthor
            },
            tokenConfig(store.getState)
            )
            .then((resp) => {
                console.log("Sent to Inbox");
            });
          })          
        });
    }
  }

  handleAcceptRequest() {
    console.log("accepting request");
    // redirect to inbox
  }

  handleDeleteFollower() {
    if (this.state.isFollower === true) {
      const foreignAuthorId = this.parseData(this.state.selectedAuthor);
      const authorId = this.props.auth.user.author;

      axios
        .delete(
          `/author/${foreignAuthorId}/followers/${authorId}`,
          tokenConfig(store.getState),
          {}
        )
        .then((resp) => {
          this.setState({
            open: false,
          });
        });
      // delete inbox request
    }
  }

  redirectToProfile(data) {
    const id = this.parseData(data);
    const path = "/profile/" + id;
    this.setState({
      redirect: path,
    });
  }

  handleCloseDialog() {
    this.setState(this.init_state);
  }
  checkLikedPost(likes) {
    const { user } = this.props;
    for (const like of likes) {
      if (like.author.id.split("/").pop() == user.user.author) {
        return true;
      }
    }
    return false;
  }

  likePost(post) {
    const { user } = this.props;

    axios
      .post(
        `/author/${post.author_id}/post/${post.id.split("/").pop()}/likes`,
        null,
        tokenConfig(store.getState)
      )
      .then((res) => {
        const likes = post.likes;
        post.likes = [
          ...likes,
          {
            type: "Like",
            author: {
              id: user.user.author,
              type: "author",
              displayName: user.user.displayName,
            },
            object: post.id,
            "@context": "https://www.w3.org/ns/activitystreams",
            summary: `${user.user.displayName} Likes your post`,
          },
        ];
        store.dispatch({
          type: LIKE_POST,
          payload: post,
        });
        store.dispatch({
          type: CREATE_ALERT,
          payload: {
            msg: { success: "Post has been liked!" },
            status: res.status,
          },
        });
      })
      .catch((e) => {
        console.log(e);
      });
  }

  render() {
    const { posts, deletePost, getPosts, user } = this.props;

    return (
      <Fragment>
        {this.state.redirect !== "" && <Redirect to={this.state.redirect} />}
        <h2>Local Public Feed</h2>

        {posts.posts.map((post) => (
          <div className="card mb-4 flex-row" key={post.id.split("/").pop()}>
            <div className="card-header mx-auto justify-content-center">
              <h2 className="text-primary mb-4">
                {this.checkLikedPost(post.likes) ? (
                  <FaThumbsUp />
                ) : (
                  <div
                    onClick={() => {
                      this.likePost(post);
                    }}
                  >
                    <FaRegThumbsUp />
                  </div>
                )}
              </h2>

              <h2 className="text-secondary mt-4">{post.likes.length}</h2>
            </div>
            <div className="card-body">
              <div className="small text-muted">
                <span className="float-end">
                  <FaRegClock />
                  &nbsp;<Moment fromNow>{post.published}</Moment>
                </span>
                <span onClick={() => this.onAuthorClick(post.author)}>
                  @{post.author.displayName}
                </span>
              </div>
              <h2 className="card-title h4">{post.title}</h2>
              <p className="card-text">{post.description}</p>
              <Link
                to={`/posts/${post.author_id}/${post.id.split("/").pop()}`}
                className="btn btn-outline-primary"
              >
                View full post →
              </Link>
              {post.author_id == user.user.author ? (
                <button
                  className="btn btn-danger float-end"
                  onClick={deletePost.bind(this, post.id)}
                >
                  <FaTrashAlt />
                </button>
              ) : (
                ""
              )}
            </div>
          </div>
        ))}
        <nav aria-label="Posts pagination">
          <ul className="pagination">
            <li className={`page-item ${!posts.previous ? "disabled" : ""}`}>
              <a
                className="page-link"
                href="#"
                aria-label="Previous"
                onClick={(e) => {
                  e.preventDefault();
                  getPosts(posts.previous);
                }}
              >
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li className="page-item active">
              <a className="page-link" href="#">
                {posts.page}
              </a>
            </li>
            <li className={`page-item ${!posts.next ? "disabled" : ""}`}>
              <a
                className="page-link"
                href="#"
                aria-label="Next"
                onClick={(e) => {
                  e.preventDefault();
                  getPosts(posts.next);
                }}
              >
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
          </ul>
        </nav>
        <Dialog open={this.state.open} onClose={() => this.handleCloseDialog()}>
          <div className="d-flex flex-row">
            <div className="p-3">
              {this.state.isFollower ? "Accept Request?" : "Send a Request"}
            </div>
            <div className="p-3">
              <div className="d-flex flex-row-reverse">
                <div onClick={() => this.handleCloseDialog()}>
                  <FaWindowClose />
                </div>
              </div>
            </div>
          </div>

          {!this.state.isFollower && (
            <div className="d-flex flex-row justify-content-center">
              <DialogContent>
                @{this.state.selectedAuthor.displayName}
              </DialogContent>
              <div className="d-flex flex-row justify-content-center">
                <DialogActions>
                  <div className="p-2">
                    <div
                      onClick={() =>
                        this.redirectToProfile(this.state.selectedAuthor)
                      }
                    >
                      <FaUserAlt />
                    </div>
                  </div>
                  <div className="p-2">
                    <div onClick={() => this.handleFollow()}>
                      <FaUserPlus />
                    </div>
                  </div>
                </DialogActions>
              </div>
            </div>
          )}

          {this.state.isFollower && (
            <div className="text-center">
              <DialogContent>
                @{this.state.selectedAuthor.displayName}
              </DialogContent>
              <div className="d-flex flex-row justify-content-center">
                <DialogActions>
                  <div
                    className="p-2"
                    onClick={() => this.handleDeleteFollower()}
                  >
                    <FaRegTrashAlt />
                  </div>
                  <div
                    className="p-2"
                    onClick={() => this.handleAcceptRequest()}
                  >
                    <FaRegEnvelope />
                  </div>
                </DialogActions>
              </div>
            </div>
          )}
        </Dialog>
      </Fragment>
    );
  }

  static propTypes = {
    posts: PropTypes.object.isRequired,
    getPosts: PropTypes.func.isRequired,
    deletePost: PropTypes.func.isRequired,
    addFollower: PropTypes.func.isRequired,
    auth: PropTypes.object.isRequired,
  };
}

const mapStateToProps = (state) => ({
  posts: state.posts,
  followers: state.followers,
  user: state.auth,
  auth: state.auth,
});

export default connect(mapStateToProps, { getPosts, deletePost, addFollower })(
  Feed
);
