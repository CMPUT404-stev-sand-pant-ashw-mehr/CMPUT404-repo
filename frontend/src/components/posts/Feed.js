import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { getPosts, deletePost } from "../../actions/posts";

import Create from "./Create";

export class Feed extends Component {
  componentDidMount() {
    this.props.getPosts();
  }

  render() {
    return (
      <Fragment>
        <h1>Feed</h1>

        {this.props.posts.map((post) => (
          <div className="card" key={post.id}>
            <div className="card-body">
              <h5 className="card-title">{post.title}</h5>
              <p className="card-text">{post.description}</p>
              <a href={post.source} className="btn btn-primary">
                Source
              </a>
              <button
                className="btn btn-danger"
                onClick={this.props.deletePost.bind(this, post.id)}
              >
                Delete Post
              </button>
            </div>
          </div>
        ))}

        <Create />
      </Fragment>
    );
  }

  static propTypes = {
    posts: PropTypes.array.isRequired,
    getPosts: PropTypes.func.isRequired,
    deletePost: PropTypes.func.isRequired,
  };
}

const mapStateToProps = (state) => ({
  posts: state.posts.posts,
});

export default connect(mapStateToProps, { getPosts, deletePost })(Feed);
