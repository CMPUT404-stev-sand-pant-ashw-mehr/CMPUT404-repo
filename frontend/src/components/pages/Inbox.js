import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import PropTypes, { object } from "prop-types";
import axios from "axios";
import { FiSend } from "react-icons/fi";
import { tokenConfig } from "../../actions/auth";
import store from "../../store";
import { FaRegClock } from "react-icons/fa";
import Moment from "react-moment";
import { Link } from "react-router-dom";

import { AiOutlineCheck, AiOutlineClose } from "react-icons/ai";

export class Inbox extends Component {
  state = {
    currentUser: this.props.auth.user,
    requests: [],
    posts: [],
    likes: [],

    friends: [],
    open: false,
    selectedFriends: {},
    selectedPost: {},
  };

  fetchFriends() {
    axios
      .get(
        `/author/${this.state.currentUser.author}/friends`,
        tokenConfig(store.getState)
      )
      .then((response) => {
        this.setState({
          friends: response.data.items,
        });
      });
  }

  fetchRequests() {
    axios
      .get(
        `/author/${this.state.currentUser.author}/inbox`,
        tokenConfig(store.getState)
      )
      .then((resp) => {
        let reqs = [],
          psts = [],
          lks = [];
        const items = resp.data.items;
        items.map((item) => {
          if (item.type === "follow") {
            reqs.push(item);
          } else if (item.type === "post") {
            psts.push(item);
          } else if (item.type === "Like") {
            lks.push(item);
          }
        });
        this.setState({
          requests: reqs,
          posts: psts,
          likes: lks,
        });
        this.setState({
          requests: reqs,
        });
      });
  }

  componentDidMount() {
    this.fetchRequests();
    this.fetchFriends();
  }

  parseData(data) {
    const parseData = data.id.split("/");
    return parseData[parseData.length - 1];
  }

  handleSend() {
    Object.keys(this.state.selectedFriends).map((friendId) => {
      let id = this.parseData(this.state.selectedFriends[friendId]);

      axios
        .post(
          `/author/${id}/inbox`,
          {
            type: "post",
            title: this.state.selectedPost.title,
            id: this.state.selectedPost.id,
            source: this.state.selectedPost.source,
            origin: this.state.selectedPost.origin,
            description: this.state.selectedPost.description,
            contentType: this.state.selectedPost.contentType,
            content: this.state.selectedPost.content,
            published: this.state.selectedPost.published,
            author: this.state.selectedPost.author,
            categories: this.state.selectedPost.categories,
            visibility: this.state.selectedPost.visibility,
            unlisted: this.state.selectedPost.unlisted,
          },
          tokenConfig(store.getState)
        )
        .then((resp) => {
          this.setState({
            open: false,
          });
        });
    });
  }

  handleSendPost(post) {
    this.setState({
      open: true,
      selectedPost: post,
    });
  }

  handleSelection(friend) {
    let selectedFriendsIds = Object.keys(this.state.selectedFriends);
    if (selectedFriendsIds.includes(friend.id)) {
      let selections = this.state.selectedFriends;
      delete selections[friend.id];
      this.setState({
        selected: selections,
      });
    } else {
      let selections = this.state.selectedFriends;
      selections[friend.id] = friend;
      this.setState({
        selected: selections,
      });
    }
  }

  handleAccept(request) {
    const foreignAuthorId = this.parseData(request.actor);
    const authorId = this.parseData(request.object);

    axios
      .put(
        `/author/${authorId}/followers/${foreignAuthorId}`,
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
      `/author/${foreignAuthorId}/followers/${authorId}`,
      tokenConfig(store.getState))
      .then((resp)=>{

      axios
      .delete(`/author/${authorId}/inbox/${foreignAuthorId}`,
        tokenConfig(store.getState),{})
        .then((resp)=>{
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

        <div className="card mt-5">
          <div className="card-header">
            <h4>Likes</h4>
          </div>
          <div className="card=body">
            {this.state.likes.map((like) => (
              <div className="card m-3 p-3">
                {like.summary} (Post ID: {like.object.split("/")[6].substr(27)})
                <span className="float-end">
                  <Link
                    to={`/posts/${like.object.split("/")[4]}/${
                      like.object.split("/")[6]
                    }`}
                    className="btn btn-outline-primary"
                  >
                    View post →
                  </Link>
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="card mt-5">
          <div className="card-header">
            <h4>Friend Posts</h4>
          </div>
          {this.state.posts.map((post) => (
            <div
              className="card mb-4 flex-row m-3"
              key={post.id.split("/").pop()}
            >
              <div className="card-header mx-auto justify-content-center"></div>
              <div className="card-body">
                <div className="small text-muted">
                  <span className="float-end">
                    <FaRegClock />
                    &nbsp;<Moment fromNow>{post.published}</Moment>
                  </span>
                  <span>@{post.author.displayName}</span>
                </div>
                <h2 className="card-title h4">{post.title}</h2>
                <p className="card-text">{post.description}</p>
                <Link
                  to={`/posts/${this.parseData(post.author)}/${post.id
                    .split("/")
                    .pop()}`}
                  className="btn btn-outline-primary"
                >
                  View full post →
                </Link>
                <button
                  type="button"
                  className="btn btn-primary float-end"
                  onClick={() => this.handleSendPost(post)}
                  data-bs-toggle="modal"
                  data-bs-target="#sendPost"
                >
                  <FiSend />
                </button>
              </div>
            </div>
          ))}
        </div>
        {this.state.open && (
          <div
            className="modal fade"
            id="sendPost"
            tabIndex="-1"
            aria-labelledby="exampleModalLabel"
            aria-hidden="true"
          >
            <div className="modal-dialog">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title" id="exampleModalLabel">
                    Send To:
                  </h5>
                </div>
                <div className="modal-body">
                  {this.state.friends.map((friend, i) => (
                    <div className="card">
                      <div className="card-body">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="checkbox"
                            name="friends"
                            value={friend.displayName}
                            id={friend.id}
                            onClick={() => this.handleSelection(friend)}
                          />
                          <label className="form-check-label" for={friend.id}>
                            @{friend.displayName}
                          </label>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    data-bs-dismiss="modal"
                  >
                    Close
                  </button>
                  <button
                    type="button"
                    className="btn btn-primary"
                    onClick={() => this.handleSend()}
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
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
