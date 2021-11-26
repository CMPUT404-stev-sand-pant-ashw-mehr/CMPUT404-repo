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

export class Feed extends Component {

  state = {
    selectedAuthor: {},
    open: false,
  };

  componentDidMount() {
    this.props.getPosts();
  }

  onAuthorClick(author){
    // check if the selected author is a follower,
    let parseData = author.id.split("/");
    const id = parseData[parseData.length - 1];
    let isFollower = this.props.checkFollower(id);
    
    this.setState({
      selectedAuthor: author,
      open: true,
    });
    console.log("is follower - ", isFollower);
  }

  handleFollow(){
    console.log("follow");
  }

  handleCloseDialog() {
    this.setState({
      selectedAuthor: "",
      open: false,
    });
  }

  render() {
    const { posts, deletePost, getPosts } = this.props;

    return (
      <Fragment>
        <h2>Local Public Feed</h2>

        {posts.posts.map((post) => (
          <div className="card mb-4" key={post.id.split("/").pop()}>
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
            <Button onClick={() => this.handleFollow()}>
              Follow  
            </Button>
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
  };
}

const mapStateToProps = (state) => ({
  posts: state.posts,
});

export default connect(mapStateToProps, { getPosts, deletePost, checkFollower, addFollower })(Feed);
