import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { getPosts, deletePost } from "../../actions/posts";
import { checkFollower, addFollower} from "../../actions/followers";

import Moment from "react-moment";
import { FaRegClock, FaTrashAlt } from "react-icons/fa";

import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContentText from "@mui/material/DialogContentText";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import Button from "@mui/material/Button";

import axios from "axios";

export class Feed extends Component {

  init_state = {
    selectedAuthor: {},
    isFollower: false,
    open: false,
  };

  state = this.init_state;
  
  tokenConfig = {
    headers:{
      "Content-Type": "application/json",
      "Authorization": "Token " + this.props.auth.token,
    }
  }

  parseData(data) {
    const parseData = data.id.split("/");
    return parseData[parseData.length - 1];
  }

  componentDidMount() {
    this.props.getPosts();
  }

  onAuthorClick(foreignAuthor){

    this.setState({
      selectedAuthor: foreignAuthor,
    })

    const auth = this.props.auth;

    const foreignAuthorId = this.parseData(foreignAuthor);

    axios.get(
      `/author/${auth.user.author}/followers/${foreignAuthorId}`, this.tokenConfig)
      .then((resp) => {
        console.log("check- ",resp);
        this.setState({
          isFollower:resp.data.detail,
          open: true,
        });
      });
  }

  handleFollow(){
    if(this.state.isFollower === false){
      const foreignAuthorId = this.parseData(this.state.selectedAuthor);
      const authorId = this.props.auth.user.author;

      axios.put(
        `/author/${foreignAuthorId}/followers/${authorId}`, this.tokenConfig)
        .then((resp) => {
          console.log("resp - ", resp);
        });
    }
  }

  handleCloseDialog() {
    this.setState(this.init_state);
  }

  render() {
    // console.log("props - ", this.props);
    const { posts, deletePost, getPosts } = this.props;

    return (
      <Fragment>
        <h1>My Feed</h1>

        {posts.posts.map((post) => (
          <div className="card mb-4" key={post.id.split("/").pop()}>
            <div className="card-body">
              <div className="small text-muted">
                <span className="float-end">
                  <FaRegClock />
                  &nbsp;<Moment fromNow>{post.published}</Moment>
                </span>
                <span onClick={() => this.onAuthorClick(post.author)}>@{post.author.displayName}</span>
              </div>
              <h2 className="card-title h4">{post.title}</h2>
              <p className="card-text">{post.description}</p>
              <Link
                to={`/posts/${post.id.split("/").pop()}`}
                className="btn btn-outline-primary"
              >
                View full post →
              </Link>
              <button
                className="btn btn-danger float-end"
                onClick={deletePost.bind(this, post.id)}
              >
                <FaTrashAlt />
              </button>
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
        <Dialog
          open={this.state.open}
          onClose={() => this.handleCloseDialog()}
        >
          <DialogTitle>{this.state.selectedAuthor.displayName}</DialogTitle>
          <DialogContent>{this.state.selectedAuthor.displayName}</DialogContent>
          <DialogActions>
            {!this.state.isFollower && <Button onClick={() => this.handleFollow()}>
              Follow  
            </Button>}
            <Button onClick={() => this.handleCloseDialog()}>
              Close
            </Button>
          </DialogActions>
        </Dialog>
      </Fragment>
    );
  }

  static propTypes = {
    posts: PropTypes.object.isRequired,
    getPosts: PropTypes.func.isRequired,
    deletePost: PropTypes.func.isRequired,
    checkFollower: PropTypes.func.isRequired,
    addFollower: PropTypes.func.isRequired,
    auth: PropTypes.object.isRequired,
  };
}

const mapStateToProps = (state) => ({
  posts: state.posts,
  followers: state.followers,
  auth: state.auth,
});

export default connect(mapStateToProps, { getPosts, deletePost, checkFollower, addFollower })(Feed);
