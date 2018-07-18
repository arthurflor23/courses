import React from 'react';
import {View, StyleSheet, WebView} from 'react-native';

const AUTHORIZATION_URL = 'https://login-project-developer-edition.na53.force.com/services/oauth2/authorize';
const CLIENT_ID = '3MVG9oNqAtcJCF.FQ3puC1hnrmzCHQapX3KwhgKnwuYgiUSiZoSAu4tYwOWsiv7V2F0ZXqs64U70kkNuI6fKg';
const CALLBACK = encodeURIComponent('LoginProject:///sfdc/auth/done');
const authUrl = `${AUTHORIZATION_URL}?response_type=token&client_id=${CLIENT_ID}&redirect_uri=${CALLBACK}`;

export default class Login extends React.Component {

  render() {
    return (
      <View style={styles.container}>
        <WebView
          source={{ uri: authUrl }}
          javaScriptEnabled
          startInLoadingState
        />
      </View>
    )
  }

}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  }
});
