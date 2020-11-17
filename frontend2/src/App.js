import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {

  constructor(props){
    super(props);
    this.state = {
      emails: [],
      searchEmail: "",
      date: Date,
      from: "",
      subject: "",
      id: "",
      labelIds: [],
      threadId: ""

    };

    this.allEmail = this.allEmail.bind(this);
    this.searchEmail = this.searchEmail.bind(this);

  }

  componentDidMount() {
    //get all entities -GET
    fetch("http://127.0.0.1:5000/api/all", {
      "method": "GET",
    })
   .then(response => response.json())
   .then(data => {
   		console.log(data)
	   	this.setState({
	   		 emails: data
	   	})
   	})
    .catch(
      err => {
        console.log(err);
    })

  
  }

  allEmail(e){

    e.preventDefault();

    fetch("http://127.0.0.1:5000/api/all", {
      "method": "GET",
      "headers": {
        //what do I put here
      },
      "body": JSON.stringify({
        date: this.state.date,
        from: this.state.from,
        subject: this.state.subject,
        id: this.state.id,
        labelIds: this.state.labelIds,
        threadId: this.state.threadId
      })
    })
    .then(response => response.json())
    .then(response => {
      console.log(response);
    })
    .catch(err=> {console.log(err);})
  }

  searchEmail(e){
    e.preventDefault();

    fetch("http://127.0.0.1:5000/api/search", {
      "method": "GET",
      "headers": {

      },
      "body": JSON.stringify({
        date: this.state.date,
        from: this.state.from,
        subject: this.state.subject,
        id: this.state.id,
        labelIds: this.state.labelIds,
        threadId: this.state.threadId
      })
    })
    .then(response => response.json())
    .then(response => {
      console.log(response);
    })
    .catch(err => {
      console.log(err);
    })
  }

  handleChange(changeObject) {
    this.setState(changeObject);
  }

  render(){
    return (
    <>
    <h1> Email Deliverability Tester </h1>
    <h2> Step 1: </h2>
    <h3> Send your emails to: nupudave89@gmail.com </h3>
    <h2> Step 2: </h2> 
    <h3> Search or check below for information about your emails </h3>
    # search bar
    <form className="d-flex flex-column">
      <legend className="text-center">Enter the Email you want to see below</legend>
      <label htmlFor="name">
        Search Email:
        <input
        searchEmail="searchEmail"
        id="searchEmail"
        type="text"
        className="form-control"
        value={this.state.searchEmail}
        onChange={(e) => this.handleChange({ name: e.target.value })}
        required
        />
        </label>
    </form>
    <p>this is my data </p>
    {this.state.emails && this.state.emails.map(email=>{
      return <tr>
        <h3>Hi</h3>
        <td>{email.from}</td>
        <td>{email.subject}</td>
      </tr>
    })}

    # carasole with emails


    </>
  );
  }
}
export default App;
