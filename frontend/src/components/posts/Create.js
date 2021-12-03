import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { createPost } from "../../actions/posts";

export class Create extends Component {
  constructor(props) {
    super(props);
    this.state = {
      title: "",
      source: "https://social-dis.herokuapp.com/",
      origin: "https://social-dis.herokuapp.com/",
      description: "",
      contentType: "text/plain",
      content: "",
      visibility: "PUBLIC",
      unlisted: false,
      imagePreview: null,
      img: null,
      base64: null
    };

    this.onImageChange = this.onImageChange.bind(this);
    this.chooseFile = React.createRef();
  }

  onImageChange = e => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      this.setState({ img: e.target.files[0] }, () => {
        console.log('img: ', this.state.img);
        
        this.getBase64(this.state.img)
          .then((res) => {
            this.setState({ content: res })
          })
          .catch(err => {
            console.log('failed', err);
          })
        this.setState({ imagePreview: URL.createObjectURL(this.state.img) });
      })
    }
  };

  getBase64 = (file) => {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    return new Promise(resolve => {
      reader.onload = e => {
        resolve(e.target.result);
      }
    })
  };

  showOpenFileDlg = () => this.chooseFile.current.click()

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
  };

  onChange = (e) => this.setState({ [e.target.name]: e.target.value, });

  onSubmit =  (e) => {
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
          {/* <div className="form-group">
            <label>Source</label>
            <input
              disabled
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
              disabled
              className="form-control"
              type="text"
              name="origin"
              onChange={this.onChange}
              value={origin}
            />
          </div> */}
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
              <option value="text/markdown">text/markdown</option>
              <option value="image">image</option>
            </select>
          </div>
          <div className="form-group">
            <label>Content</label>
            {
              contentType === "text/plain" || contentType === "text/markdown"
              ?
              <textarea
                className="form-control"
                id="content"
                name="content"
                onChange={this.onChange}
                rows="4"
                value={content}
              />
              :
              <div>
                <button variant="outlined" color="primary" onClick={this.showOpenFileDlg}>Choose Image</button>
                <br />
                <input type="file" ref={this.chooseFile} onChange={this.onImageChange} style={{ display: 'none' }} accept="image/png, image/jpeg" />
                <img style={{width:'50%'}} src={this.state.imagePreview} alt="Unavailable" />
              </div>
            }
            
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
              <option value="FRIEND">FRIEND</option>
              <option value="PRIVATE">PRIVATE</option>
              
            </select>
          </div>
          <br></br>
          <div className="form-group">
            <button onClick={this.onSubmit} className="btn btn-primary">
              Submit
            </button>
          </div>
      </div>
    );
  }

  static propTypes = {
    createPost: PropTypes.func.isRequired,
  };
}

export default connect(null, { createPost })(Create);
