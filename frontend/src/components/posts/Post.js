import React, { Component, Fragment, useState, useEffect } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { getPost, createPostComment } from "../../actions/posts";
import Moment from "react-moment";
import { FaRegClock, FaArrowUp, FaArrowDown } from "react-icons/fa";
import ReactMarkDown from "react-markdown";
import axios from "axios";

export class Post extends Component {
  state = {
    commentContent: "",
    author: null,
    showComments: false,
    comments: [],
  };

  renderPostContent = () => {
    const { post } = this.props;
    switch (post.contentType) {
      case "text/plain":
        return <p>{post.content}</p>;
      case "text/markdown":
        return <ReactMarkDown>{post.content}</ReactMarkDown>;
      case "image":
        return (
          <img style={{ width: "80%" }} src={post.content} alt="Unavailable" />
        );
      default:
        return <p>{post.content}</p>;
    }
  };

  // resetForm() {
  //   this.setState({
  //     commentContent: "",
  //   });
  // }

  onChange = (e) =>
    this.setState({
      [e.target.name]: e.target.value,
    });

  getAuhorDetail = () => {
    axios
      .get(`/author/${this.props.auth.user.author}`, {
        auth: { username: "socialdistribution_t03", password: "c404t03" },
      })
      .then((res) => {
        this.setState({
          author: res.data,
        });
      })
      .catch((error) => {
        console.log("error: ", error);
      });
  };

  onSubmit = (e) => {
    e.preventDefault();
    const { commentContent } = this.state;
    const comment = {
      author: this.state.author,
      type: "comment",
      contentType: "text/markdown",
      comment: commentContent,
    };

    this.props.createPostComment(
      this.props.match.params.authorId,
      this.props.match.params.postId,
      comment
    );
    // this.forceUpdate();
    this.setState({ commentContent: "" });
  };

  componentDidMount() {
    this.setState({
      currentUser: this.props.auth.user.author,
    });
    this.props.getPost(
      this.props.match.params.authorId,
      this.props.match.params.postId
    );
    this.getAuhorDetail();
  }

  getComments = () => {
    axios
      .get(this.props.post.comments, {
        auth: { username: "socialdistribution_t03", password: "c404t03" },
        params: {
          user: this.state.currentUser,
        },
      })
      .then((res) => {
        this.setState({ comments: res.data.comments });
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  toggleComment = () => {
    const { showComments } = this.state;
    if (showComments) {
      this.setState({ showComments: !showComments, comments: [] });
    } else {
      this.getComments();
      this.setState({ showComments: !showComments });
    }
  };

  render() {
    const { post, commentContent } = this.props;
    const { showComments } = this.state;
    return (
      post && (
        <Fragment>
          <div className="card">
            <div className="card-header">
              @{post.author.displayName}
              <span className="float-end">
                <FaRegClock />
                &nbsp;<Moment fromNow>{post.published}</Moment>
              </span>
            </div>
            <div className="card-body">
              <h5 className="card-title">{post.title}</h5>
              <p className="card-text">{post.description}</p>
              {this.renderPostContent()}
              <a href="#" className="btn btn-primary">
                Go somewhere
              </a>
            </div>
            <div className="card-footer">
              Source: <em>{post.source}</em>
            </div>
          </div>
          <div className="card mt-4">
            <div className="card-body">
              <form onSubmit={this.onSubmit}>
                <h5 className="card-title">Add a comment</h5>
                <p className="card-text">
                  <input
                    className="form-control"
                    placholder="Add a comment"
                    type="text"
                    name="commentContent"
                    onChange={this.onChange}
                    value={this.state.commentContent}
                  />
                </p>
                <button type="submit" className="btn btn-primary">
                  Post
                </button>
              </form>
            </div>
          </div>
          <div>
            <button
              className="btn btn-outline-primary mt-4 btn-sm"
              onClick={this.toggleComment}
            >
              {!showComments ? (
                <div>
                  Show Comments <FaArrowDown />
                </div>
              ) : (
                <div>
                  Hide Comments <FaArrowUp />
                </div>
              )}
            </button>
            {showComments &&
              this.state.comments.map((item, index) => (
                <div
                  key={index}
                  className={
                    index == this.state.comments.length - 1
                      ? "card mt-2 mb-5"
                      : "card mt-2"
                  }
                >
                  <div className="card-header">
                    @{item.author.displayName}
                    <h6 className="card-text secondary float-end">
                      <Moment fromNow>{item.published}</Moment>
                    </h6>
                  </div>
                  <div className="card-body">
                    <p className="card-text">{item.comment}</p>
                  </div>
                </div>
              ))}
          </div>
          <br />
          {post.commentsSrc.comments &&
            post.commentsSrc.comments.map((comment) => (
              <div key={comment.id}>
                <div className="card">
                  <div className="card-body">
                    <b>{comment.author.displayName}</b>
                    <p>{comment.comment} </p>
                  </div>
                </div>
                <br />
              </div>
            ))}
        </Fragment>
      )
    );
  }

  static propTypes = {
    post: PropTypes.object.isRequired,
    getPost: PropTypes.func.isRequired,
    createPostComment: PropTypes.func.isRequired,
  };
}

const mapStateToProps = (state) => ({
  post: state.post.post,
  auth: state.auth,
});

export default connect(mapStateToProps, {
  getPost,
  createPostComment,
})(Post);
