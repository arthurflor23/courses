import React, {Component} from 'react';
import {View, AsyncStorage, Linking, StyleSheet} from 'react-native';
import * as querystring from 'query-string';

import Login from './pages/Login';
import Home from './pages/Home';

export default class App extends Component {

  state = {
    loggedIn: false,
  }
  
  async componentWillMount() {
    const logged = JSON.parse(await AsyncStorage.getItem('@LoginProject:loggedIn'));
    console.log('Logged: ', logged);
    
    this.setState({loggedIn: logged ? true : false});
  }

  componentDidMount() {
    Linking.addEventListener('url', this.handleOauthCallback);
  }

  componentWillUnmount() {
    Linking.removeEventListener('url', this.handleOauthCallback);
  }

  handleOauthCallback = async (event) => {
    console.log('Callback called!!');
    const loginInfo = querystring.parse(event.url.split('#')[1]);
    
    this.setState({loggedIn: true});
    await AsyncStorage.setItem('@LoginProject:instanceUrl', loginInfo.instance_url);
    await AsyncStorage.setItem('@LoginProject:accessToken', loginInfo.access_token);
    await AsyncStorage.setItem('@LoginProject:loggedIn', JSON.stringify(this.state.loggedIn));
  }

  render() {
    return (
      <View style={styles.container}>
        {!this.state.loggedIn && <Login />}
        {this.state.loggedIn && <Home />}
      </View>
    );
  }

}

const styles = StyleSheet.create({
  container: {
    flex: 1,    
  }
})
