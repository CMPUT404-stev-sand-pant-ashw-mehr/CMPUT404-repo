import React, { Component } from "react";
import { connect } from "react-redux";
import { tokenConfig } from "../../actions/auth";
import axios from "axios";
import store from "../../store";
import { CREATE_ALERT } from "../../actions/types";
import { Link } from "react-router-dom";
import auth from "../../reducers/auth";

class AuthorSearch extends Component {
  state = {
    authors: [],
    isLoading: false,
    loadingText: "",
    followers: [],
    followings: [],

    page: 1,
    offset: 0,
    limit: 5,
  };

  componentDidMount = () => {
    const { auth } = this.props;
    this.setState({ isLoading: true, loadingText: "Loading..." });
    axios
      .get(`/authors`, tokenConfig(store.getState))
      .then((res) => {
        this.setState({
          authors: res.data.items,
        });

        axios
          .get(
            `/author/${auth.user.author}/followings`,
            tokenConfig(store.getState)
          )
          .then((resp) => {
            this.setState({
              followings: resp.data.items,
            });

            axios
              .get(
                `/author/${auth.user.author}/followers`,
                tokenConfig(store.getState)
              )
              .then((respo) => {
                this.setState({
                  followers: respo.data.items,
                  isLoading: false,
                  loadingText: "",
                });
              });
          });
      })
      .catch((err) => {
        console.log(err);
        this.setState({
          isLoading: false,
          loadingText: "Error",
        });
      });
  };

  isFollower(foreignAuthor) {
    const { auth } = this.props.auth;

    const foreignAuthorId = foreignAuthor.id.split("/").pop();

    axios
      .get(
        `/author/${auth.user.author}/followers/${foreignAuthorId}`,
        tokenConfig(store.getState)
      )
      .then((resp) => {
        console.log(resp.data.detail);
      });
  }

  handleFollow(author) {
    if (
      this.determineType(author.id) == "Follow!" ||
      this.determineType(author.id) == "Follower"
    ) {
      const foreignAuthorId = author.id.split("/").pop();
      const authorId = this.props.auth.user.author;

      axios
        .put(
          `/author/${foreignAuthorId}/followers/${authorId}`,
          {},
          tokenConfig(store.getState)
        )
        .then((response) => {
          this.setState({
            open: false,
          });
          axios
            .get(`/author/${authorId}`, tokenConfig(store.getState))
            .then((resp) => {
              axios
                .post(
                  `/author/${foreignAuthorId}/inbox`,
                  {
                    type: "follow",
                    summary: `${resp.data.displayName} wants to follow ${author.displayName}`,
                    actor: resp.data, //author,
                    object: author, //foreignAuthor
                  },
                  tokenConfig(store.getState)
                )
                .then((resp) => {
                  store.dispatch({
                    type: CREATE_ALERT,
                    payload: {
                      msg: { success: "Follow request has been sent!" },
                      status: resp.status,
                    },
                  });
                });
            });
        });
    } else {
      store.dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { error: "You are already following that author!" },
          status: 400,
        },
      });
    }
  }

  determineType(authorId) {
    let isFollower =
      this.state.followers.filter((follower) => follower.id === authorId)
        .length > 0;
    let isFollowing =
      this.state.followings.filter((following) => following.id === authorId)
        .length > 0;

    let type = "Follow!";
    if (isFollower && !isFollowing) {
      type = "Follower";
    } else if (!isFollower && isFollowing) {
      type = "Following";
    } else if (isFollower && isFollowing) {
      type = "Friends";
    }

    return type;
  }

  determineTypeClass(authorId) {
    return this.determineType(authorId) == "Follow!"
      ? "col-md-2 float-end btn btn-primary"
      : "col-md-2 float-end btn btn-outline-primary";
  }

  showPreviousAuthors() {
    this.setState({
      page: this.state.page - 1,
      limit: this.state.offset,
      offset: this.state.offset - 5,
    });
  }

  showNextAuthors() {
    this.setState({
      page: this.state.page + 1,
      offset: this.state.limit,
      limit: this.state.limit + 5,
    });
  }

  render() {
    const { authors, isLoading, offset, limit, page, followers, following } =
      this.state;
    const { auth } = this.props;
    return (
      <div>
        <h2>Find an Author</h2>
        {isLoading ? (
          <h5 className="mt-3">{this.state.loadingText}</h5>
        ) : (
          authors
            .filter((author) => author.id.split("/").pop() != auth.user.author)
            .map((author, index) => (
              <div
                className="card"
                style={{
                  marginTop: 10,
                  marginBottom: 10,
                  padding: 10,
                }}
                key={index}
              >
                <div>
                  <Link
                    className="text-decoration-none text-dark"
                    to={`/profile/${author.id.split("/").pop()}`}
                  >
                    {author.displayName}
                  </Link>
                </div>

                <div>
                  <button
                    class={this.determineTypeClass(author.id)}
                    onClick={() => this.handleFollow(author)}
                  >
                    {this.determineType(author.id)}
                  </button>
                </div>

                <div>{author.host}</div>
              </div>
            ))
            .slice(this.state.offset, this.state.limit)
        )}

        {!isLoading && (
          <nav aria-label="Posts pagination">
            <ul className="pagination">
              <li className={`page-item ${page == 1 ? "disabled" : ""}`}>
                <button
                  className="page-link"
                  aria-label="Next"
                  onClick={this.showPreviousAuthors.bind(this)}
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
                  authors.length < limit ? "disabled" : ""
                }`}
              >
                <button
                  className="page-link"
                  aria-label="Next"
                  onClick={this.showNextAuthors.bind(this)}
                >
                  <span aria-hidden="true">&raquo;</span>
                </button>
              </li>
            </ul>
          </nav>
        )}
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  auth: state.auth,
});

export default connect(mapStateToProps)(AuthorSearch);
