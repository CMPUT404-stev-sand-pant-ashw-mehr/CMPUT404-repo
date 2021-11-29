import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { getAuthorPosts, deletePost } from "../../actions/posts";
import Moment from "react-moment";
import { FaRegClock, FaTrashAlt } from "react-icons/fa";
import { tokenConfig } from "../../actions/auth";
import axios from "axios";
import store from "../../store";

export class Profile extends Component {
  constructor(props) {
    super(props);

    this.state = {
      displayName: "",
      url: "",
      host: "",
      github: "",
    };
  }

  componentDidMount() {
    this.props.getAuthorPosts(this.props.match.params.id);

    var self = this;
    axios
      .get(`/author/${this.props.match.params.id}`, tokenConfig(store.getState))
      .then((res) => {
        self.setState({
          displayName: res.data.displayName,
          url: res.data.url,
          host: res.data.host,
          github: res.data.github,
        });
      })
      .catch((e) => {
        console.log(e);
      });
  }

  render() {
    const { posts, deletePost, user, match } = this.props;
    const { displayName, url, host, github } = this.state;

    return (
      <Fragment>
        <h2>User Details</h2>
        <div>
          <p>Username: {displayName}</p>
          <p>Author URL: {url}</p>
          <p>Github: {github}</p>
          <p>Host: {host}</p>
        </div>
        <br />
        <hr />
        <br />
        <h2>Posts by this User</h2>

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
                to={`/posts/${post.author_id}/${post.id.split("/").pop()}`}
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
                  getPosts(match.params.id, posts.previous);
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
                  getPosts(match.params.id, posts.next);
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
    getAuthorPosts: PropTypes.func.isRequired,
    deletePost: PropTypes.func.isRequired,
  };
}

const mapStateToProps = (state) => ({
  posts: state.authorposts,
  user: state.auth,
});

export default connect(mapStateToProps, { getAuthorPosts, deletePost })(
  Profile
);
