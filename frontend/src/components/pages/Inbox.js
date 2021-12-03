import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes, { object } from "prop-types";
import { getPosts, deletePost } from "../../actions/posts";
import { addFollower } from "../../actions/followers";
import { CREATE_ALERT, LIKE_POST } from "../../actions/types";
import axios from "axios";
import { tokenConfig } from "../../actions/auth";
import store from "../../store";
import { ThemeConsumer } from "styled-components";
import post from "../../reducers/post";

import { AiOutlineCheck, AiOutlineClose } from "react-icons/ai";                    

export class Inbox extends Component {
    state = {
        currentUser: this.props.auth.user,
        requests: [],
        posts: [],
        likes: [],
    }

  componentDidMount() {
      axios.get(`/author/${this.state.currentUser.author}/inbox`,
        tokenConfig(store.getState)
      )
      .then((resp) => {
          const items = resp.data.items;
          items.map((item)=>{
            if(item.type==="follow"){
                let reqs = [...this.state.requests];
                reqs.push(item);
                this.setState({
                    requests: reqs
                });
            }
            else if(item.type==="post"){
                let reqs = [...this.state.posts];
                reqs.push(item);
                this.setState({
                    posts: reqs
                });
            };
          });
      })

  }

  parseData(data) {
    const parseData = data.id.split("/");
    return parseData[parseData.length - 1];
  }

  
  handleAccept(request, index) {
      // foreign - actor
      // me - object
      const foreignAuthorId = this.parseData(request.actor);
      const authorId = this.parseData(request.object);

      axios
        .put(
          `/author/${foreignAuthorId}/followers/${authorId}`,
          {},
          tokenConfig(store.getState)
        )
        .then((response) => {
            let reqs = [...this.state.requests];
            reqs.splice(idx, 1);
            this.setState({
                request: reqs
            });
        });
    }

  handleClear() {
    // const foreignAuthorId = this.parseData(request.actor);
    // const authorId = this.parseData(request.object);

    axios.delete(`/author/${this.state.currentUser.author}/inbox`,
          tokenConfig(store.getState),{}
        )
        .then((response) => {
          console.log("Inbox Cleared");
        //   this.state.requests.map((request)=>{
        //       this.handleDeleteFollower(request.actor, request.object)
        //   })
        });
    }


  render() {

    return (
      <Fragment>
        <h2>Inbox</h2>

        <div className="card">
        <div className="card-header">
            <h2>Friend Requests</h2>
            {this.state.requests.length>0 && <button className="btn btn-primary float-end" onClick={()=>this.handleClear()}>
                Clear Inbox
            </button>}
        </div>
            {this.state.requests.length>0 && this.state.requests.map((request, idx) => (
            <div className="card flex-row">
                <div className="card-body">
                    <p className="card-text">@{request.actor.displayName} wants to be your friend
                    <div className="float-end p-2">
                        <button className="btn btn-success" onClick={()=>this.handleAccept(request, idx)}>
                            < AiOutlineCheck />
                        </button>
                    </div>
                    </p>

                </div>
            </div>
            ))}
            {this.state.requests.length===0 && <div className="card flex-row">
                <div className="card-body">
                    <p className="card-text">No friend requests</p>
                </div>
            </div>}
        </div>

        {/* {this.state.posts.map((post) => (
          <div className="card mb-4 flex-row" key={post.id.split("/").pop()}>
            <div className="card-header mx-auto justify-content-center">
              <h2 className="text-primary mb-4">
                {this.checkLikedPost(post.likes) ? (
                  <FaThumbsUp />
                ) : (
                  <div
                    onClick={() => {
                      this.likePost(post);
                    }}
                  >
                    <FaRegThumbsUp />
                  </div>
                )}
              </h2>

              <h2 className="text-secondary mt-4">{post.likes.length}</h2>
            </div>
            <div className="card-body">
              <div className="small text-muted">
                <span className="float-end">
                  <FaRegClock />
                  &nbsp;<Moment fromNow>{post.published}</Moment>
                </span>
                <span onClick={() => this.onAuthorClick(post.author)}>
                  @{post.author.displayName}
                </span>
              </div>
              <h2 className="card-title h4">{post.title}</h2>
              <p className="card-text">{post.description}</p>
              <Link
                to={`/posts/${post.author_id}/${post.id.split("/").pop()}`}
                className="btn btn-outline-primary"
              >
                View full post →
              </Link>
              {post.author_id == user.user.author ? (
                <button
                  className="btn btn-danger float-end"
                  onClick={deletePost.bind(this, post.id)}
                >
                  <FaTrashAlt />
                </button>
              ) : (
                ""
              )}
            </div>
          </div>
        ))} */}
        
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

export default connect(mapStateToProps)(
  Inbox
);
