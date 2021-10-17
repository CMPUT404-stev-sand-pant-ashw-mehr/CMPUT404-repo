import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { createPost } from "../../actions/posts";

export class Create extends Component {
  state = {
    type: "",
    title: "",
    source: "",
    origin: "",
    description: "",
    contentType: "",
    content: "",
    visibility: "",
    unlisted: false,
  };

  onChange = (e) =>
    this.setState({
      [e.target.name]: e.target.value,
    });

  onSubmit = (e) => {
    e.preventDefault();
    const {
      type,
      title,
      source,
      origin,
      description,
      contentType,
      content,
      visibility,
    } = this.state;
    const post = {
      postType: type,
      author: 1,
      title,
      source,
      origin,
      description,
      contentType,
      content,
      visibility,
      unlisted: false,
    };
    this.props.createPost(post);
  };

  render() {
    const {
      type,
      title,
      source,
      origin,
      description,
      contentType,
      content,
      visibility,
    } = this.state;

    return (
      <div>
        <form onSubmit={this.onSubmit}>
          <div class="form-group">
            <label>Type</label>
            <input
              className="form-control"
              type="text"
              name="type"
              onChange={this.onChange}
              value={type}
            />
          </div>
          <div class="form-group">
            <label>Title</label>
            <input
              className="form-control"
              type="text"
              name="title"
              onChange={this.onChange}
              value={title}
            />
          </div>
          <div class="form-group">
            <label>Source</label>
            <input
              className="form-control"
              type="text"
              name="source"
              onChange={this.onChange}
              value={source}
            />
          </div>
          <div class="form-group">
            <label>Origin</label>
            <input
              className="form-control"
              type="text"
              name="origin"
              onChange={this.onChange}
              value={origin}
            />
          </div>
          <div class="form-group">
            <label>Description</label>
            <input
              className="form-control"
              type="text"
              name="description"
              onChange={this.onChange}
              value={description}
            />
          </div>
          <div class="form-group">
            <label>Content Type</label>
            <input
              className="form-control"
              type="text"
              name="contentType"
              onChange={this.onChange}
              value={contentType}
            />
          </div>
          <div class="form-group">
            <label>Content</label>
            <input
              className="form-control"
              type="text"
              name="content"
              onChange={this.onChange}
              value={content}
            />
          </div>
          <div class="form-group">
            <label>Visibility</label>
            <input
              className="form-control"
              type="text"
              name="visibility"
              onChange={this.onChange}
              value={visibility}
            />
          </div>
          <div class="form-group">
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </div>
        </form>
      </div>
    );
  }

  static propTypes = {
    createPost: PropTypes.func.isRequired,
  };
}

export default connect(null, { createPost })(Create);
