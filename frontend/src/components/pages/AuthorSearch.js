import React, { Component } from "react";
import { connect } from "react-redux";
import axios from "axios";

class AuthorSearch extends Component {
  state = {
    authors: [],
    isLoading: false,
    loadingText: "",

    page: 1,
    offset: 0,
    limit: 5,
  };

  componentDidMount = () => {
    this.setState({ isLoading: true, loadingText: "Loading ..." });
    axios
      .get(`/authors`, {
        auth: { username: "socialdistribution_t03", password: "c404t03" },
      })
      .then((res) => {
        console.log(res.data.items);
        this.setState({
          authors: res.data.items,
          isLoading: false,
          loadingText: "",
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
    const { authors, isLoading, offset, limit, page } = this.state;

    return (
      <div>
        <h2>Find an Author</h2>
        {isLoading ? (
          <h4>{this.state.loadingText}</h4>
        ) : (
          authors
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
                {author.displayName}
                <br />
                {author.host}
              </div>
            ))
            .slice(this.state.offset, this.state.limit)
        )}

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
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  auth: state.auth,
});

export default connect(mapStateToProps)(AuthorSearch);
