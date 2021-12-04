import React, { Component } from 'react'
import { connect } from "react-redux";
import axios from "axios";

class GitHub extends Component {

    state = {
        activities:[],
        isLoading:false,
        loadingText:"",

        page: 1,
        offset: 0,
        limit: 5,
    }

    componentDidMount = () => {
        console.log('GitHub:',this.props);
        this.setState({isLoading:true, loadingText:'Loading ...'})
        axios.get(`/author/${this.props.auth.user.author}/github`,{auth:{username:'socialdistribution_t03', password:'c404t03'}})
        .then(res => {
            console.log(res.data);
            this.setState({activities:res.data,isLoading:false, loadingText:""});
        })
        .catch(err => {
            this.setState({activities:res.data,isLoading:false, loadingText:"Error"});
        })
    }

    showPreviousPosts() {
        this.setState({
            page: this.state.page - 1,
            limit: this.state.offset,
            offset: this.state.offset - 5,
        });
    }

    showNextPosts() {
        this.setState({
            page: this.state.page + 1,
            offset: this.state.limit,
            limit: this.state.limit + 5,
        });
    }

    render() {
        const {activities,isLoading, offset, limit, page} = this.state;
        
        return (
            <div>
                <h1>Github Activity</h1>
                {
                    isLoading ? <h3>{this.state.loadingText}</h3> :
                    activities.map((activity, index)=> 
                    <div style={{border:'1px solid #a5a5a5', borderRadius:'5px', margin:10, padding:10}} key={index}>

                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
                            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                        </svg>

                        <br/>
                        <span style={{fontWeight:500}}>
                         Activity Type: </span> {activity.type}
                        <br />
                        <span style={{fontWeight:500}}>Created At: </span> {activity.created_at}
                        <br />
                        <span style={{fontWeight:500}}>Repo: </span> {activity.repo.name}
                        <br />
                    </div>
                    ).slice(this.state.offset, this.state.limit)
                }

                <nav aria-label="Posts pagination">
                    <ul className="pagination">
                        <li className={`page-item ${page == 1 ? "disabled" : ""}`}>
                        <button
                            className="page-link"
                            aria-label="Next"
                            onClick={this.showPreviousPosts.bind(this)}
                        >
                            <span aria-hidden="true">&laquo;</span>
                        </button>
                        </li>
                        <li className="page-item active">
                        <a className="page-link" href="#">
                            {page}
                        </a>
                        </li>
                        <li
                        className={`page-item ${
                            activities.length < limit ? "disabled" : ""
                        }`}
                        >
                        <button
                            className="page-link"
                            aria-label="Next"
                            onClick={this.showNextPosts.bind(this)}
                        >
                            <span aria-hidden="true">&raquo;</span>
                        </button>
                        </li>
                    </ul>
                </nav>

            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    auth: state.auth,
  });
  

export default connect(mapStateToProps)(GitHub)