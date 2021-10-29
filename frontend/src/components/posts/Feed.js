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
    const { posts, deletePost, getPosts } = this.props;

    return (
      <Fragment>
        <h1>My Feed</h1>

        {posts.posts.map((post) => (
          <div className="card mb-4">
            <div className="card-body">
              <div className="small text-muted">4 mins ago</div>
              <h2 className="card-title h4">{post.title}</h2>
              <p className="card-text">{post.description}</p>
              <a className="btn btn-primary" href="#">
                View full post →
              </a>
              <button
                className="btn btn-danger float-end"
                onClick={deletePost.bind(this, post.id)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
        <nav aria-label="Page navigation example">
          <ul className="pagination">
            <li className={`page-item ${!posts.previous ? "disabled" : ""}`}>
              <a
                className="page-link"
                href="#"
                aria-label="Previous"
                onClick={() => {
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
                onClick={() => {
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
});

export default connect(mapStateToProps, { getPosts, deletePost })(Feed);
