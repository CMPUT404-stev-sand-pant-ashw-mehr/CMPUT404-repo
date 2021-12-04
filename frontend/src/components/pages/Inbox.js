import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import PropTypes, { object } from "prop-types";
import axios from "axios";
import { tokenConfig } from "../../actions/auth";
import store from "../../store";

import { AiOutlineCheck, AiOutlineClose } from "react-icons/ai";

export class Inbox extends Component {
  state = {
    currentUser: this.props.auth.user,
    requests: [],
    posts: [],
    likes: [],
  };

  fetchRequests() {
    axios
      .get(
        `/author/${this.state.currentUser.author}/inbox`,
        tokenConfig(store.getState)
      )
      .then((resp) => {
        let reqs = [];
        const items = resp.data.items;
        items.map((item) => {
          if (item.type === "follow") {
            reqs.push(item);
          }
        });
        this.setState({
          requests: reqs,
        });
      });
  }

  componentDidMount() {
    this.fetchRequests();
  }

  parseData(data) {
    const parseData = data.id.split("/");
    return parseData[parseData.length - 1];
  }

  handleAccept(request) {
    const foreignAuthorId = this.parseData(request.actor);
    const authorId = this.parseData(request.object);

    axios
      .put(
        `/author/${foreignAuthorId}/followers/${authorId}`,
        {},
        tokenConfig(store.getState)
      )
      .then((response) => {
        axios
          .delete(
            `/author/${authorId}/inbox/${foreignAuthorId}`,
            tokenConfig(store.getState),
            {}
          )
          .then((resp) => {
            this.fetchRequests();
          });
      });
  }

  handleReject(request) {
    const foreignAuthorId = this.parseData(request.actor);
    const authorId = this.parseData(request.object);
    axios
      .delete(
        `/author/${authorId}/followers/${foreignAuthorId}`,
        tokenConfig(store.getState),
        {}
      )
      .then((resp) => {
        axios
          .delete(
            `/author/${authorId}/inbox/${foreignAuthorId}`,
            tokenConfig(store.getState),
            {}
          )
          .then((resp) => {
            this.fetchRequests();
          });
      });
  }

  handleClear() {
    axios
      .delete(
        `/author/${this.state.currentUser.author}/inbox`,
        tokenConfig(store.getState),
        {}
      )
      .then((response) => {
        this.fetchRequests();
      });
  }

  render() {
    return (
      <Fragment>
        <h2>Inbox</h2>

        <div className="card">
          <div className="card-header">
            <h4>Friend Requests</h4>
            {this.state.requests.length > 0 && (
              <button
                className="btn btn-primary float-end"
                onClick={() => this.handleClear()}
              >
                Clear Inbox
              </button>
            )}
          </div>
          {this.state.requests.length > 0 &&
            this.state.requests.map((request) => (
              <div className="card flex-row">
                <div className="card-body">
                  <p className="card-text">
                    @{request.actor.displayName} wants to be your friend
                    <div className="float-end p-2">
                      <button
                        className="btn btn-success"
                        onClick={() => this.handleAccept(request)}
                      >
                        <AiOutlineCheck />
                      </button>
                    </div>
                    <div className="float-end p-2">
                      <button
                        className="btn btn-danger"
                        onClick={() => this.handleReject(request)}
                      >
                        <AiOutlineClose />
                      </button>
                    </div>
                  </p>
                </div>
              </div>
            ))}
          {this.state.requests.length === 0 && (
            <div className="card flex-row">
              <div className="card-body">
                <p className="card-text">No friend requests</p>
              </div>
            </div>
          )}
        </div>
      </Fragment>
    );
  }

  static propTypes = {
    auth: PropTypes.object.isRequired,
  };
}

const mapStateToProps = (state) => ({
  auth: state.auth,
});

export default connect(mapStateToProps)(Inbox);
