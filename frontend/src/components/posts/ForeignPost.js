import React, { Component, Fragment, useState, useEffect } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { getForeignPost } from "../../actions/posts";
import Moment from "react-moment";
import { FaRegClock } from "react-icons/fa";
import ReactMarkDown from "react-markdown";

export class ForeignPost extends Component {
  state = {
    commentContent: "",
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

  onChange = (e) =>
    this.setState({
      [e.target.name]: e.target.value,
    });

  onSubmit = (e) => {
    e.preventDefault();
    const { commentContent } = this.state;
    const comment = {
      type: "comment",
      contentType: "text/markdown",
      comment: commentContent,
    };

    // this.props.createPostComment(this.props.match.params.postId, comment);
    console.log("send to inbox");
    this.resetForm();
    this.forceUpdate();
  };

  componentDidMount() {
    this.props.getForeignPost(this.props.match.params.postId);
  }

  render() {
    const { post, commentContent } = this.props;
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
});

export default connect(mapStateToProps, {
  getForeignPost,
})(ForeignPost);
