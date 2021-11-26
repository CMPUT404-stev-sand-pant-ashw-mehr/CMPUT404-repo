import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { getPosts, deletePost } from "../../actions/posts";
import Moment from "react-moment";
import { tokenConfig } from "../../actions/auth";
import axios from "axios";
import store from "../../store";
import { CREATE_ALERT, LIKE_POST } from "../../actions/types";
import {
  FaRegClock,
  FaTrashAlt,
  FaRegThumbsUp,
  FaThumbsUp,
} from "react-icons/fa";

export class Feed extends Component {
  componentDidMount() {
    this.props.getPosts();
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
                <Link
                  to={`/profile/${post.author_id}`}
                  className="text-decoration-none text-secondary"
                >
                  @{post.author.displayName}
                </Link>
              </div>
              <h2 className="card-title h4">{post.title}</h2>
              <p className="card-text">{post.description}</p>
              <Link
                to={`/posts/${post.id.split("/").pop()}`}
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
      </Fragment>
    );
  }

  static propTypes = {
    posts: PropTypes.object.isRequired,
    getPosts: PropTypes.func.isRequired,
    deletePost: PropTypes.func.isRequired,
  };
}

const mapStateToProps = (state) => ({
  posts: state.posts,
  user: state.auth,
});

export default connect(mapStateToProps, { getPosts, deletePost })(Feed);
