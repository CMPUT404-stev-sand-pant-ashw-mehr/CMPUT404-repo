import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { getForeignPosts, deletePost } from "../../actions/posts";
import Moment from "react-moment";
import { FaRegClock, FaTrashAlt } from "react-icons/fa";

export class ForeignFeed extends Component {
  constructor(props) {
    super(props);

    this.state = {
      page: 1,
      offset: 0,
      limit: 5,
    };
  }

  showPreviousPosts() {
    this.setState({
      page: this.state.page - 1,
      limit: this.state.offset,
      offset: this.state.offset - 5,
    });
  }

  showNextPosts() {
    this.setState({
      page: this.state.page + 1,
      offset: this.state.limit,
      limit: this.state.limit + 5,
    });
  }

  componentDidMount() {
    this.props.getForeignPosts();
  }

  renderHost(authorHost) {
    var url = new URL(authorHost);
    return url.host;
  }

  render() {
    const { posts } = this.props;
    const { offset, limit, page } = this.state;
    let paginatedposts = posts.posts
      .sort(function (a, b) {
        return new Date(b.published) - new Date(a.published);
      })
      .slice(this.state.offset, this.state.limit);

    return (
      <Fragment>
        <h2>Foreign Feed</h2>

        {paginatedposts.map((post) => (
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
                to={`/foreign/posts/${post.id.split("/").pop()}`}
                className="btn btn-outline-primary"
              >
                View full post →
              </Link>
              <span className="badge bg-secondary float-end">
                {this.renderHost(post.author.host)}
              </span>
            </div>
          </div>
        ))}
        <nav aria-label="Posts pagination">
          <ul className="pagination">
            <li className={`page-item ${page == 1 ? "disabled" : ""}`}>
              <button
                className="page-link"
                aria-label="Next"
                onClick={this.showPreviousPosts.bind(this)}
              >
                <span aria-hidden="true">&laquo;</span>
              </button>
            </li>
            <li className="page-item active">
              <a className="page-link" href="#">
                {page}
              </a>
            </li>
            <li
              className={`page-item ${
                posts.posts.length < limit ? "disabled" : ""
              }`}
            >
              <button
                className="page-link"
                aria-label="Next"
                onClick={this.showNextPosts.bind(this)}
              >
                <span aria-hidden="true">&raquo;</span>
              </button>
            </li>
          </ul>
        </nav>
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
