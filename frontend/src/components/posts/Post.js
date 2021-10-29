import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { getPost } from "../../actions/posts";
import Moment from "react-moment";
import { FaRegClock } from "react-icons/fa";

export class Post extends Component {
  componentDidMount() {
    this.props.getPost(this.props.match.params.id);
  }

  render() {
    const { post } = this.props;

    return (
      post && (
        <Fragment>
          <div class="card">
            <div class="card-header">
              @{post.author.displayName}
              <span className="float-end">
                <FaRegClock />
                &nbsp;<Moment fromNow>{post.published}</Moment>
              </span>
            </div>
            <div class="card-body">
              <h5 class="card-title">{post.title}</h5>
              <p class="card-text">{post.description}</p>
              <p>{post.content}</p>
              <a href="#" class="btn btn-primary">
                Go somewhere
              </a>
            </div>
            <div className="card-footer">
              Source: <em>{post.source}</em>
            </div>
          </div>
          <br />
          {post.commentsSrc.comments &&
            post.commentsSrc.comments.map((comment) => (
              <div key={comment.id}>
                <div class="card">
                  <div class="card-body">{comment.comment}</div>
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
  };
}

const mapStateToProps = (state) => ({
  post: state.post.post,
});

export default connect(mapStateToProps, { getPost })(Post);
