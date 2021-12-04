import React, { Component, Fragment, useState, useEffect } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { getPost, createPostComment } from "../../actions/posts";
import Moment from "react-moment";
import { FaRegClock } from "react-icons/fa";
import ReactMarkDown from "react-markdown";
import axios from "axios";

export class Post extends Component {
  state = {
    commentContent: "",
    author: null,
    showComments: false,
    comments:[]
  };

  renderPostContent = () => {
    
    const { post } = this.props;
    switch (post.contentType) {
      case "text/plain":
        return <p>{post.content}</p>;
      case "text/markdown":
        return <ReactMarkDown>{post.content}</ReactMarkDown>;
      case "image":
        return <img style={{width:'80%'}} src={post.content} alt="Unavailable" />
      default:
        return <p>{post.content}</p>;
    }
  }

  resetForm() {
    this.setState({
      commentContent: "",
    });
  }

  onChange = (e) =>
    this.setState({
      [e.target.name]: e.target.value,
    });
  
  getAuhorDetail = () => {
    axios.get(`/author/${this.props.auth.user.author}`, {auth:{username:'socialdistribution_t03', password:'c404t03'}})
    .then((res)=>{
      // console.log("data: ");
      // console.log(res.data);
      this.setState({
        author: res.data
      })
    }).catch((error)=>{
      console.log("error: ", error);
    })
  }
  

  onSubmit = (e) => {
    e.preventDefault();
    const { commentContent } = this.state;
    console.log("author: ", this.state.author)
    const comment = {
      author: this.state.author,
      type: "comment",
      contentType: "text/markdown",
      comment: commentContent,
    };

    this.props.createPostComment(this.props.match.params.authorId, this.props.match.params.postId, comment);
    this.resetForm();
    this.forceUpdate();
  };

  componentDidMount() {
    this.props.getPost(
      this.props.match.params.authorId,
      this.props.match.params.postId,
    );
    this.getAuhorDetail()
  }

  getComments = () => {
    axios.get(this.props.post.comments, {auth:{username:'socialdistribution_t03',password:'c404t03'}})
    .then(res => {
      console.log(res.data.comments);
      this.setState({ comments: res.data.comments })
    })
    .catch(err => {
      console.log(err.message);
    });
  }

  toggleComment = () => {
    const { showComments } = this.state;
    if (showComments) {
      this.setState({ showComments:!showComments, comments:[] });
    } else {
      this.getComments();
      this.setState({ showComments:!showComments });
    }
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
          <div>
          <button className="btn btn-primary" style={{margin:20}} onClick={this.toggleComment}> show comments </button>
          {this.state.comments.map((item, index)=> 
            <div style={{margin:10, border:'1px solid #a6a6a6'}} key={index} className="card">
              <div className="card-header">@{item.author.displayName}</div>
              <div className="card-body">
                <p className="card-text" style={{fontSize:25}}>{item.comment}</p>
                <p className="card-text secondary" style={{fontSize:10}}>Created at {item.published}</p>
              </div>
            </div>
          )
          }
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
