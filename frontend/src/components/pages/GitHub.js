import React, { Component } from 'react'
import { connect } from "react-redux";
import axios from "axios";

class GitHub extends Component {

    state = {
        activities:[],
        isLoading:false,
        loadingText:""
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

    render() {
        const {activities,isLoading} = this.state;
        return (
            <div>
                <h1>Github</h1>
                {
                    isLoading ? <h3>{this.state.loadingText}</h3> :
                    activities.map((activity, index)=> 
                    <div style={{border:'1px solid #a5a5a5', borderRadius:'5px', margin:10, padding:10}} key={index}>
                        <span style={{fontWeight:500}}>Activity Type: </span> {activity.type}
                        <br />
                        <span style={{fontWeight:500}}>Created At: </span> {activity.created_at}
                        <br />
                        <span style={{fontWeight:500}}>Repo: </span> {activity.repo.name}
                        <br />
                    </div>
                    )
                }
            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    auth: state.auth,
  });
  

export default connect(mapStateToProps)(GitHub)