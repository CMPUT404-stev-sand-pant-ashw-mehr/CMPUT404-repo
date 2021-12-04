import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { getAuthorPosts, deletePost, sendPost } from "../../actions/posts";
import Moment from "react-moment";
import { FaRegClock, FaTrashAlt } from "react-icons/fa";
import { FiSend } from "react-icons/fi";
import { tokenConfig } from "../../actions/auth";
import axios from "axios";
import store from "../../store";
// import Checkbox from "@material-ui/core/Checkbox";

export class Profile extends Component {
  constructor(props) {
    super(props);
  }

  state = {
    displayName: "",
    url: "",
    host: "",
    github: "",
    showEdit: false,
    newDisplayedName:"",
    newGitHub:"",

    friends: [],
    open: false,
    selectedFriends: {},
    selectedPost:{}

  };

  componentDidMount() {
    this.props.getAuthorPosts(this.props.match.params.id);
    this.getUserProfile();
  }

  
  parseData(data) {
    const parseData = data.id.split("/");
    return parseData[parseData.length - 1];
  }

  getUserProfile = () => {
    var self = this;
    axios
      .get(`/author/${this.props.match.params.id}`, tokenConfig(store.getState))
      .then((res) => {
        axios.get(`/author/${this.props.match.params.id}/friends`, tokenConfig(store.getState))
        .then((response)=>{
          this.setState({
            displayName: res.data.displayName,
            url: res.data.url,
            host: res.data.host,
            github: res.data.github,
            friends: response.data.items,
          });
        })
      })
      .catch((e) => {
        console.log(e);
      });
    }

  handleSend(){
    console.log(this.state.selectedFriends);
    console.log(this.state.selectedPost);
    Object.keys(this.state.selectedFriends).map((friendId)=>{
      let id = this.parseData(this.state.selectedFriends[friendId]);
      
      axios.post(`/author/${id}/inbox`,
            {
              "type":"post",
              "title":this.state.selectedPost.title ,
              "id":this.state.selectedPost.id,
              "source":this.state.selectedPost.source,
              "origin":this.state.selectedPost.origin,
              "description":this.state.selectedPost.description,
              "contentType":this.state.selectedPost.contentType,
              "content":this.state.selectedPost.content,
              "published":this.state.selectedPost.published,
              "author":this.state.selectedPost.author,
              "categories":this.state.selectedPost.categories,
              "visibility":this.state.selectedPost.visibility,
              "unlisted":this.state.selectedPost.unlisted,
            },
            tokenConfig(store.getState)
            )
            .then((resp) => {
                console.log("Sent to Inbox");
                this.setState({
                  open: false,
                })
          });
    })
  }

  handleSendPost(post){
    // console.log("selected - ", this.state.selectedFriends);
    this.setState({
      open: true,
      selectedPost: post,
    });
  }

  handleSelection(friend){
    let selectedFriendsIds = Object.keys(this.state.selectedFriends);
    if(selectedFriendsIds.includes(friend.id)){
      let selections = this.state.selectedFriends;
      delete selections[friend.id];
      this.setState({
        selected: selections,
      });
    }else{
      let selections = this.state.selectedFriends;
      selections[friend.id] = friend;
      // selections.push(friendId);
      this.setState({
      selected: selections,
    });
    }
  }

  render() {
    const { posts, deletePost, sendPost, user, match } = this.props;
    const { displayName, url, host, github, friends, showEdit } = this.state;

    return (
      <Fragment>
        <h2>User Details</h2>
        <div style={{fontStyle:'italic', fontWeight:500}}>
          <p>Welcome, {displayName} !</p>
          <p>Author URL: {url}</p>
          <p>Github: {github}</p>
          <p>Host: {host}</p>
        </div>
        <br />
        <button onClick={this.toggleEdit}>{showEdit ? "Cancel":"Edit"}</button>
        {
          showEdit ? 
          <div style={{border:"1px solid #a7a7a7", borderRadius:'5px', margin: 25}}>
            <div style={{margin:30}}>
              <label>Display Name:</label>
              <br/>
              <input type="text" placeholder="Enter your new displayed name" onChange={(e)=>this.setState({newDisplayedName:e.target.value})}/>
            </div>
            <br/>
            <div style={{margin:30}}>
              <label>GitHub:</label>
              <br/>
              <input type="text" placeholder="Enter your Github" onChange={(e)=> this.setState({newGitHub:e.target.value})} />
            </div>
            <br/>

            <button style={{margin: 30}} onClick={this.updateProfile}>Submit Change</button>
          </div> 
          : 
          null
        }
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
              <div className="p-2">
                <button type="button" className="btn btn-primary float-end" onClick={()=>this.handleSendPost(post)} data-bs-toggle="modal" data-bs-target="#sendPost">
                  <FiSend />
                </button>
                <button
                  className="btn btn-danger float-end"
                  onClick={deletePost.bind(this, post.id)}
                >
                  <FaTrashAlt />
                </button>
              </div>
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

        {this.state.open && <div className="modal fade" id="sendPost" tabIndex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="exampleModalLabel">Send To:</h5>
              </div>
              <div className="modal-body">
              {friends.map((friend,i) => <div className="card">
                          <div className="card-body">
                            <div className="form-check">
                              <input className="form-check-input" type="checkbox" name="friends" value={friend.displayName} id={friend.id} onClick={()=>this.handleSelection(friend)}/>
                              <label className="form-check-label" for={friend.id}>
                                @{friend.displayName}
                              </label>
                            </div>
                          </div>
                      </div>)}

                {/* {friends.map((friend,i) => <li key={i}>{friend.displayName}</li>)} */}
              {/* {this.state.requests.length>0 && this.state.requests.map((request) => ( */}
                  {/* {friends.map((friend)=>{
                      <div className="card">
                          <div className="card-body">
                            <div className="form-check">
                              <input className="form-check-input" type="checkbox" name="friends" value={friend.displayName} id={friend.id} onClick={()=>this.handleSelection(friend.id)}/>
                              <label className="form-check-label" for={friend.id}>
                                @{friend.displayName}
                                hello
                              </label>
                            </div>
                          </div>
                      </div>
                    })} */}
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" className="btn btn-primary" onClick={()=>this.handleSend()}>Send</button>
              </div>
            </div>
          </div>
        </div>}
      </Fragment>
    );
  }

  static propTypes = {
    posts: PropTypes.object.isRequired,
    getAuthorPosts: PropTypes.func.isRequired,
    deletePost: PropTypes.func.isRequired,
    sendPost: PropTypes.func.isRequired,
  };
}

const mapStateToProps = (state) => ({
  posts: state.authorposts,
  friends: state.friends,
  user: state.auth,
});

export default connect(mapStateToProps, { getAuthorPosts, deletePost, sendPost })(
  Profile
);
