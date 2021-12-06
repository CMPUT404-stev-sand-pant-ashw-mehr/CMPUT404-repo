import React, { Component, Fragment, useState, useEffect } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { getForeignPost } from "../../actions/posts";
import Moment from "react-moment";
import { FaRegClock } from "react-icons/fa";
import ReactMarkDown from "react-markdown";
import axios from "axios";
import { tokenConfig } from "../../actions/auth";
import store from "../../store";
import { CREATE_ALERT } from "../../actions/types";
import post from "../../reducers/post";

export class ForeignPost extends Component {
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
      case "image/png;base64":
      case "image/jpeg;base64":
      case "image/png":
      case "image/jpeg":
        return (
          <img style={{ width: "80%" }} src={post.content} alt="Unavailable" />
        );
      default:
        return <p>{post.content}</p>;
    }
  };

  resetForm() {
    this.setState({
      commentContent: "",
    });
  }

  getComments = () => {
    axios
      .post(
        `/connection/comments`,
        { commentsUrl: this.props.post.comments },
        tokenConfig(store.getState)
      )
      .then((res) => {
        this.setState({
          comments:
            res.data != "There are no comments on the post" ? res.data : [],
        });
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

  onChange = (e) =>
    this.setState({
      [e.target.name]: e.target.value,
    });

  onSubmit = (e) => {
    const { post } = this.props;

    e.preventDefault();
    const { commentContent } = this.state;
    const comment = {
      type: "comment",
      contentType: "text/markdown",
      comment: commentContent,
    };

    axios
      .post(
        `/connection/${this.props.auth.user.author}/comment/${post.id
          .split("/")
          .pop()}/${comment.comment}`,
        null,
        tokenConfig(store.getState)
      )
      .then((res) => {
        store.dispatch({
          type: CREATE_ALERT,
          payload: {
            msg: { success: "Comment sent to foreign author!" },
            status: res.status,
          },
        });
      })
      .catch((e) => {
        store.dispatch({
          type: CREATE_ALERT,
          payload: {
            msg: { error: "Failed to comment on post." },
            status: 500,
          },
        });
        console.log(e);
      });

    this.resetForm();
    this.forceUpdate();
  };

  componentDidMount() {
    this.props.getForeignPost(this.props.match.params.postId);
  }

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
          <br />
          <div className="card">
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
                    value={commentContent}
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
                    @{item.authorId.displayName}
                    <h6 className="card-text secondary float-end">
                      <Moment fromNow>{item.publishedOn}</Moment>
                    </h6>
                  </div>
                  <div className="card-body">
                    <p className="card-text">{item.text}</p>
                  </div>
                </div>
              ))}
          </div>
        </Fragment>
      )
    );
  }

  static propTypes = {
    post: PropTypes.object.isRequired,
    getForeignPost: PropTypes.func.isRequired,
  };
}

const mapStateToProps = (state) => ({
  post: state.foreignpost.post,
  auth: state.auth,
});

export default connect(mapStateToProps, {
  getForeignPost,
})(ForeignPost);
