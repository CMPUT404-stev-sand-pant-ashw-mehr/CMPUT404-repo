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
  };

  componentDidMount() {
    this.props.getAuthorPosts(this.props.match.params.id);
    this.getUserProfile();
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
    this.setState({
      open: true,
    });
  }

  handleSelected(){
    console.log("in selected");
  }

  handleNotSelected(){
    console.log("in not selected");
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
                <button type="button" className="btn btn-primary float-end" onClick={()=>this.handleSend()} data-bs-toggle="modal" data-bs-target="#sendPost">
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

        <div className="modal fade" id="sendPost" tabIndex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="exampleModalLabel">Send To:</h5>
                {/* <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button> */}
              </div>
              <div className="modal-body">
                  {this.state.open && this.state.friends.map((friend)=>{
                      return <div className="card">
                          <div className="card-body">
                            <div className="form-check">
                              <input className="form-check-input" type="checkbox" value={friend.displayName} id={friend.id}/>
                              <label className="form-check-label" for={friend.id}>
                                @{friend.displayName}
                              </label>
                              {/* {checkedValue} */}

                              {/* onClick={true? ()=>{this.handleSelected()}: ()=>{this.handleNotSelected()} */}
                            </div>
                          </div>
                        </div>
                    })}
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" className="btn btn-primary">Send</button>
              </div>
            </div>
          </div>
        </div>
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
