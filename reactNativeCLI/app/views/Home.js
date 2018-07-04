import React from 'react';
import { StyleSheet, View } from 'react-native';
import { Header } from '../sections/Header';
import { Menu } from '../sections/Menu';
import { Logo } from '../sections/Logo';

export class Home extends React.Component {

  static navigationOptions = { header: null };

  render() {
    const { navigate } = this.props.navigation;

    return (
      <View style={styles.container}>
        <Header message='Press to login' />
        <Logo />
        <Menu navigate={ navigate }/>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    flex: 8,
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
});
