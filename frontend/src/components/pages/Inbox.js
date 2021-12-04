import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import PropTypes, { object } from "prop-types";
import axios from "axios";
import { tokenConfig } from "../../actions/auth";
import store from "../../store";
import {
  FaRegClock
} from "react-icons/fa";
import Moment from "react-moment";
import { Link } from "react-router-dom";

import { AiOutlineCheck, AiOutlineClose } from "react-icons/ai";                    

export class Inbox extends Component {
    state = {
        currentUser: this.props.auth.user,
        requests: [],
        posts: [],
        likes: [],
    }

    fetchRequests() {
      axios.get(`/author/${this.state.currentUser.author}/inbox`,
        tokenConfig(store.getState)
      )
      .then((resp) => {
        let reqs = [], psts=[], lks=[];
          const items = resp.data.items;
          console.log("ALL ITEMS - ", items);
          items.map((item)=>{
            if(item.type==="follow"){
                reqs.push(item);
            }
            else if(item.type==="post"){
              console.log("in post");
              psts.push(item);
            }
            else if(item.type==="like"){
              lks.push(item);
            }
          });
          this.setState({
            requests: reqs,
            posts: psts,
            likes: lks,
        });
      })

    }

  componentDidMount() {
      this.fetchRequests();
  }

  parseData(data) {
    const parseData = data.id.split("/");
    return parseData[parseData.length - 1];
  }

  checkLikedPost(likes) {
    const { user } = this.props;
    for (const like of likes) {
      if (like.author.id.split("/").pop() == user.user.author) {
        return true;
      }
    }
    return false;
  }

  likePost(post) {
    const { user } = this.props;

    axios
      .post(
        `/author/${post.author_id}/post/${post.id.split("/").pop()}/likes`,
        null,
        tokenConfig(store.getState)
      )
      .then((res) => {
        const likes = post.likes;
        post.likes = [
          ...likes,
          {
            type: "Like",
            author: {
              id: user.user.author,
              type: "author",
              displayName: user.user.displayName,
            },
            object: post.id,
            "@context": "https://www.w3.org/ns/activitystreams",
            summary: `${user.user.displayName} Likes your post`,
          },
        ];
        store.dispatch({
          type: LIKE_POST,
          payload: post,
        });
        store.dispatch({
          type: CREATE_ALERT,
          payload: {
            msg: { success: "Post has been liked!" },
            status: res.status,
          },
        });
      })
      .catch((e) => {
        console.log(e);
      });
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
          axios.delete(`/author/${authorId}/inbox/${foreignAuthorId}`,
            tokenConfig(store.getState),{}
          ).then((resp)=>{
            this.fetchRequests();
          })
        });
    }
  
  handleReject(request){
    const foreignAuthorId = this.parseData(request.actor);
    const authorId = this.parseData(request.object);
    axios
    .delete(
      `/author/${authorId}/followers/${foreignAuthorId}`,
      tokenConfig(store.getState),
      {}
    ).then((resp)=>{
      axios.delete(`/author/${authorId}/inbox/${foreignAuthorId}`,
            tokenConfig(store.getState),{}
          ).then((resp)=>{
            this.fetchRequests();
          });
    }) 
  }

  handleClear() {
    axios.delete(`/author/${this.state.currentUser.author}/inbox`,
          tokenConfig(store.getState),{}
        )
        .then((response) => {
          this.fetchRequests();
        });
    }

  show(){
    console.log(this.state.posts);
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
            {this.state.requests.length>0 && this.state.requests.map((request) => (
            <div className="card flex-row">
                <div className="card-body">
                    <p className="card-text">@{request.actor.displayName} wants to be your friend
                    <div className="float-end p-2">
                        <button className="btn btn-success" onClick={()=>this.handleAccept(request)}>
                            < AiOutlineCheck />
                        </button>
                    </div>
                    <div className="float-end p-2">
                        <button className="btn btn-danger" onClick={()=>this.handleReject(request)}>
                            < AiOutlineClose />
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

        <div className="card mt-5">
        <div className="card-header">
            <h2>Friend Posts</h2>
            <button className="btn btn-primary float-end" onClick={()=>this.show()}>
                show
            </button>
        </div>
        {this.state.posts.map((post) => (
          <div className="card mb-4 flex-row" key={post.id.split("/").pop()}>
            <div className="card-header mx-auto justify-content-center">
            </div>
            <div className="card-body">
              <div className="small text-muted">
                <span className="float-end">
                  <FaRegClock />
                  &nbsp;<Moment fromNow>{post.published}</Moment>
                </span>
                <span>
                  @{post.author.displayName}
                </span>
              </div>
              <h2 className="card-title h4">{post.title}</h2>
              <p className="card-text">{post.description}</p>
              <Link
                to={`/posts/${post.author.id}/${post.id.split("/").pop()}`}
                className="btn btn-outline-primary"
              >
                View full post →
              </Link>
            </div>
          </div>
        ))}
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

export default connect(mapStateToProps)(
  Inbox
);
