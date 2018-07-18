import React, {Component} from 'react';
import {StyleSheet, Text, View, AsyncStorage} from 'react-native';

export default class Home extends Component {

  state = {
    accessToken: null,
    instanceUrl: null,
  }

  async componentDidMount() {
    this.setState({
      instanceUrl: await AsyncStorage.getItem('@LoginProject:instanceUrl'),
      accessToken: await AsyncStorage.getItem('@LoginProject:accessToken'),
    });
  }

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.loginMessage}>Logged in!</Text>
        <View>
          <Text style={styles.message}>Instance URL</Text>
          <Text style={styles.tokenMessage}>{this.state.instanceUrl}</Text>
          <Text style={styles.message}>Access token</Text>
          <Text style={styles.tokenMessage}>{this.state.accessToken}</Text>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
    backgroundColor: 'white',
  },
  loginMessage: {
    fontSize: 30, 
    marginBottom: 30,
  },
  tokenMessage: {
    fontSize: 18, 
    marginBottom: 10,
  },
  message: {
    fontSize: 18, 
    fontWeight: 'bold',
  },
});
