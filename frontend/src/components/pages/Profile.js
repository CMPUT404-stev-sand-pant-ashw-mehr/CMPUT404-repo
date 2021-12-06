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
import { BsPeople } from "react-icons/bs";

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
    openSendPost: false,
    openShowFriends: false,
    selectedFriendsSend: {},
    selectedFriendsShow: {},
    selectedPost:{},
    currentUser: this.props.match.params.id,
  };

  toggleEdit = () => {
    const {showEdit} = this.state;
    this.setState({showEdit: !showEdit, newDisplayedName:"", newGitHub:""});
  }

  updateProfile = () => {
    const {newDisplayedName, newGitHub} = this.state;
    if (!newDisplayedName || !newGitHub) {
      alert("Check your displayed name and GitHub");
      return;
    }

    axios.post(`/author/${this.props.match.params.id}`, 
    { 
      displayName: newDisplayedName, 
      github: newGitHub
    }, 
    tokenConfig(store.getState))
    .then(res => {
      console.log('success:', res);
      this.getUserProfile()
      this.setState({
        showEdit:false,
        newDisplayedName:"",
        newGitHub:""
      })
    })
    .catch(err => {
      console.log('failed:', err.message);
    })
  }

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
    Object.keys(this.state.selectedFriendsSend).map((friendId)=>{
      let id = this.parseData(this.state.selectedFriendsSend[friendId]);
      
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
                this.setState({
                  openSendPost: false,
                })
          });
    })
  }

  handleClose(){
    // console.log(this.state.selectedFriendsShow);
    this.setState({
      openSendPost: false,
      openShowFriends: false,
      selectedFriendsSend:[],
      selectedFriendsShow:[],
    });
  }

  handleSendPost(post){
    this.setState({
      openSendPost: true,
      selectedPost: post,
    });
  }

  handleSelection(friend, mode){
    let selectedIds = [], selectedObjs = [];
    if(mode==="send"){
      selectedIds = Object.keys(this.state.selectedFriendsSend);
      selectedObjs = this.state.selectedFriendsSend;
    }
    else if(mode==="show"){
      selectedIds = Object.keys(this.state.selectedFriendsShow);
      selectedObjs = this.state.selectedFriendsShow;
    }

    if(selectedIds.includes(friend.id)){
      delete selectedObjs[friend.id];
      if(mode==="send"){
        this.setState({
          selectedFriendsSend: selectedObjs,
        });
      }
      else if(mode==="show"){
        this.setState({
          selectedFriendsShow: selectedObjs,
        });
      }
    }else{
      selectedObjs[friend.id] = friend;
      if(mode==="send"){
        this.setState({
          selectedFriendsSend: selectedObjs,
        });
      }
      else if(mode==="show"){
        this.setState({
          selectedFriendsShow: selectedObjs,
        });
      }
    }
  }

  handleShowFriends(){
    this.setState({
      openShowFriends: true,
    });
  }

  handleRemoveFriends(){
    let friends=this.state.selectedFriendsShow;

    Object.keys(friends).map((friendId)=>{
      axios
        .delete(
          `/author/${this.parseData(friends[friendId])}/followers/${this.state.currentUser}`,
          tokenConfig(store.getState),
          {}
        ).then(()=>{
          this.getUserProfile();
        })
    });
  }

  render() {
    const { posts, deletePost, sendPost, user, match } = this.props;
    const { displayName, url, host, github, friends, showEdit } = this.state;

    return (
      <Fragment>
        <div className="card mb-4">
          <div className="card-body">
            <h2 className="card-title h3">
              User Details
              <button type="button" className="btn btn-primary float-end" onClick={this.toggleEdit}>{showEdit ? "Cancel":"Edit"}</button>
            </h2>
            <div className="card mb-4">
              <div className="card-body">
                <p className="card-text">Welcome, {displayName}</p>
                <p className="card-text">Author URL: {url}</p>
                <p className="card-text">Github: {github}</p>
                <p className="card-text">Host: {host}</p>
              </div>
            </div>
            <button type="button" className="btn btn-primary float-end" onClick={()=>this.handleShowFriends()} data-bs-toggle="modal" data-bs-target="#showFriends">
              Friends <BsPeople />
            </button>
        </div>
      </div>
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

        <div className="card mb-4">
          <div className="card-body">
          <h2 className="card-title h3">Your Posts</h2>
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
          </div>
        </div>

        
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

        {this.state.openSendPost && <div className="modal fade" id="sendPost" tabIndex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="exampleModalLabel">Send To:</h5>
              </div>
              <div className="modal-body">
              {friends.map((friend,index) => <div className="card" key={index}>
                      <div className="card-body">
                        <div className="form-check">
                          <input className="form-check-input" type="checkbox" name="friends" value={friend.displayName} id={friend.id} onClick={()=>this.handleSelection(friend, "send")}/>
                          <label className="form-check-label" for={friend.id}>
                            @{friend.displayName}
                          </label>
                        </div>
                      </div>
                  </div>)}
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={()=>this.handleClose()} data-bs-dismiss="modal">Close</button>
                <button type="button" className="btn btn-primary" onClick={()=>this.handleSend()}>Send</button>
              </div>
            </div>
          </div>
        </div>}

        {this.state.openShowFriends && <div className="modal fade" id="showFriends" tabIndex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="exampleModalLabel">Friends</h5>
              </div>
              <div className="modal-body">
              {friends.map((friend,i) => <div className="card" key={friend.id}>
                      <div className="card-body">
                        <div className="form-check">
                          <input className="form-check-input" type="checkbox" name="friends" value={friend.displayName} id={friend.id} onClick={()=>this.handleSelection(friend, "show")}/>
                          <label className="form-check-label" for={friend.id}>
                            @{friend.displayName}
                          </label>
                        </div>
                      </div>
                  </div>)}
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={()=>this.handleClose()} data-bs-dismiss="modal">Close</button>
                <button type="button" className="btn btn-danger" onClick={()=>this.handleRemoveFriends()} data-bs-dismiss="modal">Delete</button>
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
