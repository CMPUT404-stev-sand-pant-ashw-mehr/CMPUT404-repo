import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { createPost } from "../../actions/posts";

export class Create extends Component {
  state = {
    title: "",
    source: "",
    origin: "",
    description: "",
    contentType: "text/plain",
    content: "",
    visibility: "PUBLIC",
    unlisted: false,
  };

  resetForm() {
    this.setState({
      title: "",
      source: "",
      origin: "",
      description: "",
      contentType: "",
      content: "",
      visibility: "",
      unlisted: false,
    });
  }

  onChange = (e) =>
    this.setState({
      [e.target.name]: e.target.value,
    });

  onSubmit = (e) => {
    e.preventDefault();
    const {
      title,
      source,
      origin,
      description,
      contentType,
      content,
      visibility,
    } = this.state;
    const post = {
      type: "POST",
      title,
      source,
      origin,
      description,
      contentType,
      content,
      visibility,
      unlisted: false,
      categories: ["web"],
    };
    this.props.createPost(post);
    this.resetForm();
  };

  render() {
    const {
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
          <div className="form-group">
            <label>Title</label>
            <input
              className="form-control"
              type="text"
              name="title"
              onChange={this.onChange}
              value={title}
            />
          </div>
          <div className="form-group">
            <label>Source</label>
            <input
              className="form-control"
              type="text"
              name="source"
              onChange={this.onChange}
              value={source}
            />
          </div>
          <div className="form-group">
            <label>Origin</label>
            <input
              className="form-control"
              type="text"
              name="origin"
              onChange={this.onChange}
              value={origin}
            />
          </div>
          <div className="form-group">
            <label>Description</label>
            <input
              className="form-control"
              type="text"
              name="description"
              onChange={this.onChange}
              value={description}
            />
          </div>
          <div className="form-group">
            <label>Content Type</label>
            <select
              className="form-control"
              type="text"
              name="contentType"
              onChange={this.onChange}
              value={contentType}
            >
              <option value="text/plain">text/plain</option>
            </select>
          </div>
          <div className="form-group">
            <label>Content</label>
            <textarea
              className="form-control"
              id="content"
              name="content"
              onChange={this.onChange}
              rows="4"
            >
              {content}
            </textarea>
          </div>
          <div className="form-group">
            <label>Visibility</label>
            <select
              className="form-control"
              type="text"
              name="visibility"
              onChange={this.onChange}
              value={visibility}
            >
              <option value="PUBLIC">PUBLIC</option>
            </select>
          </div>
          <br></br>
          <div className="form-group">
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
