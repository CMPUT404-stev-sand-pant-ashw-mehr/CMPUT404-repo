import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { getForeignPosts, deletePost } from "../../actions/posts";
import Moment from "react-moment";
import { FaRegClock, FaTrashAlt } from "react-icons/fa";

export class ForeignFeed extends Component {
  componentDidMount() {
    this.props.getForeignPosts();
  }

  renderHost(authorHost) {
    var url = new URL(authorHost);
    return url.host;
  }

  render() {
    const { posts } = this.props;

    return (
      <Fragment>
        <h2>Foreign Feed</h2>

        {posts.posts.map((post) => (
          <div className="card mb-4" key={post.id.split("/").pop()}>
            <div className="card-body">
              <div className="small text-muted">
                <span className="float-end">
                  <FaRegClock />
                  &nbsp;<Moment fromNow>{post.published}</Moment>
                </span>
                @{post.author.displayName}
              </div>
              <h2 className="card-title h4">{post.title}</h2>
              <p className="card-text">{post.description}</p>
              <Link
                to={`/posts/${post.id.split("/").pop()}`}
                className="btn btn-outline-primary float-end"
              >
                View full post →
              </Link>
              <span className="badge bg-secondary">
                {this.renderHost(post.author.host)}
              </span>
            </div>
          </div>
        ))}
      </Fragment>
    );
  }

  static propTypes = {
    posts: PropTypes.object.isRequired,
    getForeignPosts: PropTypes.func.isRequired,
  };
}

const mapStateToProps = (state) => ({
  posts: state.foreignposts,
});

export default connect(mapStateToProps, { getForeignPosts })(ForeignFeed);
