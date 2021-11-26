import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { getPosts, deletePost } from "../../actions/posts";
import { checkFollower, addFollower} from "../../actions/followers";

import Moment from "react-moment";
import { FaRegClock, FaTrashAlt } from "react-icons/fa";

import Dialog from '@mui/material/Dialog';
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
<<<<<<< HEAD
import { Redirect } from "react-router-dom";


import axios from "axios";
import { Reddit } from "@mui/icons-material";
=======
import Button from "@mui/material/Button";
import { IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
// import PersonAddIcon from '@mui/icons-material/PersonAdd';
// import MarkEmailUnreadIcon from '@mui/icons-material/MarkEmailUnread';
>>>>>>> 3b98c51 (finished follow dialog)

import axios from "axios";

export class Feed extends Component {

  init_state = {
    selectedAuthor: {},
    isFollower: false,
    open: false,
    redirect: "",
  };

  state = this.init_state;
  
  tokenConfig = {
    headers:{
      "Content-Type": "application/json",
      "Authorization": "Token " + this.props.auth.token,
    }
  }

  parseData(data) {
    const parseData = data.id.split("/");
    return parseData[parseData.length - 1];
  }

  componentDidMount() {
    this.props.getPosts();
  }

  onAuthorClick(foreignAuthor){

    this.setState({
      selectedAuthor: foreignAuthor,
    })

    const auth = this.props.auth;

    const foreignAuthorId = this.parseData(foreignAuthor);

    axios.get(
      `/author/${auth.user.author}/followers/${foreignAuthorId}`, this.tokenConfig)
      .then((resp) => {
        this.setState({
          isFollower:resp.data.detail,
          open: true,
        });
      });
  }

  handleFollow(){
    if(this.state.isFollower === false){
      const foreignAuthorId = this.parseData(this.state.selectedAuthor);
      const authorId = this.props.auth.user.author;

      axios.put(`/author/${foreignAuthorId}/followers/${authorId}`, {}, this.tokenConfig).then((response) => {
        this.setState({
          open: false,
        })
      })

      // send inbox request
<<<<<<< HEAD
=======
    }
  }

  handleAcceptRequest() {
    console.log("accepting request");
    // redirect to inbox
  }

  handleDeleteFollower(){
    if(this.state.isFollower === true){
      const foreignAuthorId = this.parseData(this.state.selectedAuthor);
      const authorId = this.props.auth.user.author;

      axios.delete(`/author/${foreignAuthorId}/followers/${authorId}`, this.tokenConfig, {}).then((resp) => {
        this.setState({
          open: false,
        })
      })
      // delete inbox request
>>>>>>> 3b98c51 (finished follow dialog)
    }
  }

  handleAcceptRequest() {
    console.log("accepting request");
    // redirect to inbox
  }

  handleDeleteFollower(){
    if(this.state.isFollower === true){
      const foreignAuthorId = this.parseData(this.state.selectedAuthor);
      const authorId = this.props.auth.user.author;

      axios.delete(`/author/${foreignAuthorId}/followers/${authorId}`, this.tokenConfig, {}).then((resp) => {
        this.setState({
          open: false,
        })
      })
      // delete inbox request
    }
  }
  
  redirectToProfile(data) {
    const id = this.parseData(data);
    const path = "/profile/"+id;
    this.setState({
      redirect: path,
    })
   
  }

  handleCloseDialog() {
    this.setState(this.init_state);
  }

  render() {
    const { posts, deletePost, getPosts } = this.props;

    return (
      <Fragment>
        {this.state.redirect!=="" && <Redirect to={this.state.redirect}/>}
        <h2>Local Public Feed</h2>

        {posts.posts.map((post) => (
          <div class="card mb-4" key={post.id.split("/").pop()}>
            <div class="card-body">
              <div class="small text-muted">
                <span class="float-end">
                  <FaRegClock />
                  &nbsp;<Moment fromNow>{post.published}</Moment>
                </span>
                <span onClick={() => this.onAuthorClick(post.author)}>@{post.author.displayName}</span>
              </div>
              <h2 class="card-title h4">{post.title}</h2>
              <p class="card-text">{post.description}</p>
              <Link
                to={`/posts/${post.id.split("/").pop()}`}
                class="btn btn-outline-primary"
              >
                View full post →
              </Link>
              <button
                class="btn btn-danger float-end"
                onClick={deletePost.bind(this, post.id)}
              >
                <FaTrashAlt />
              </button>
            </div>
          </div>
        ))}
        <nav aria-label="Posts pagination">
          <ul class="pagination">
            <li class={`page-item ${!posts.previous ? "disabled" : ""}`}>
              <a
                class="page-link"
                href="#"
                aria-label="Previous"
                onClick={(e) => {
                  e.preventDefault();
                  getPosts(posts.previous);
                }}
              >
                <span aria-hidden="true">&laquo;</span>
              </a>
            </li>
            <li class="page-item active">
              <a class="page-link" href="#">
                {posts.page}
              </a>
            </li>
            <li class={`page-item ${!posts.next ? "disabled" : ""}`}>
              <a
                class="page-link"
                href="#"
                aria-label="Next"
                onClick={(e) => {
                  e.preventDefault();
                  getPosts(posts.next);
                }}
              >
                <span aria-hidden="true">&raquo;</span>
              </a>
            </li>
          </ul>
        </nav>
        <Dialog
          open={this.state.open}
          onClose={() => this.handleCloseDialog()}
        >          
          <div class="d-flex flex-row">
            <div class="p-3">{this.state.isFollower? "Accept Request?": "Send a Request"}</div>
            <div class="p-3">
              <div class="d-flex flex-row-reverse">
<<<<<<< HEAD
                <i class="bi bi-x-lg p-2" onClick={() => this.handleCloseDialog()}></i>
=======
                <IconButton class="p-2" onClick={() => this.handleCloseDialog()}>
                    <CloseIcon />
                </IconButton>
>>>>>>> 3b98c51 (finished follow dialog)
              </div>
            </div>
          </div>

          {!this.state.isFollower && <div class="d-flex flex-row justify-content-center">
<<<<<<< HEAD

          <DialogContent>@{this.state.selectedAuthor.displayName}</DialogContent>
            <div class="d-flex flex-row justify-content-center">
              <DialogActions>
                <div class="p-2">
                <i class="bi bi-person-circle" onClick={() => this.redirectToProfile(this.state.selectedAuthor)}></i>
                  {/* <i class="bi bi-trash fa-lg" onClick={() => this.handleDeleteFollower()}></i>                   */}
                </div>
                <div class="p-2">
                  <i class="bi bi-person-plus fa-lg" onClick={() => this.handleFollow()}></i>

                  {/* <i class="bi bi-envelope-check fa-lg" onClick={() => this.handleAcceptRequest()}></i> */}
                </div>
              </DialogActions>
            </div>



            {/* <div class="p-2 text-center">
=======
            <div class="p-2 text-center">
>>>>>>> 3b98c51 (finished follow dialog)
              <DialogContent>@{this.state.selectedAuthor.displayName}</DialogContent>
            </div>
            <DialogActions>
              <div class="p-2">
<<<<<<< HEAD
                <i class="bi bi-person-circle" onClick={() => this.redirectToProfile(this.state.selectedAuthor)}></i>
              </div>
            </DialogActions>
            <i class="bi bi-person-plus fa-lg" onClick={() => this.handleFollow()}></i> */}

=======
                  <i class="bi bi-person-plus fa-lg" onClick={() => this.handleFollow()}></i>
              </div>
            </DialogActions>
>>>>>>> 3b98c51 (finished follow dialog)
          </div>}

          {this.state.isFollower && <div class="text-center">
            <DialogContent>@{this.state.selectedAuthor.displayName}</DialogContent>
            <div class="d-flex flex-row justify-content-center">
              <DialogActions>
                <div class="p-2">
                  <i class="bi bi-trash fa-lg" onClick={() => this.handleDeleteFollower()}></i>                  
                </div>
                <div class="p-2">
                  <i class="bi bi-envelope-check fa-lg" onClick={() => this.handleAcceptRequest()}></i>
                </div>
              </DialogActions>
            </div>
            </div>
          }          
        </Dialog>
      </Fragment>
    );
  }

  static propTypes = {
    posts: PropTypes.object.isRequired,
    getPosts: PropTypes.func.isRequired,
    deletePost: PropTypes.func.isRequired,
    checkFollower: PropTypes.func.isRequired,
    addFollower: PropTypes.func.isRequired,
    auth: PropTypes.object.isRequired,
  };
}

const mapStateToProps = (state) => ({
  posts: state.posts,
  followers: state.followers,
  auth: state.auth,
});

export default connect(mapStateToProps, { getPosts, deletePost, checkFollower, addFollower })(Feed);
