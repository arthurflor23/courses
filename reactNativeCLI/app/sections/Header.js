import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

export class Header extends React.Component {

  constructor(props) {
    super(props);
    this.state = { isLoggedIn: false };
  }

  render() {
    let display = this.state.isLoggedIn ? 'Simple User' : this.props.message;

    return (
      <View style={styles.headStyle}>
        <Text style={styles.headText} onPress={this.toggleUser}> {display} </Text>
      </View>
    );
  };

  toggleUser = () => {
    this.setState((previousState) => {
      return { isLoggedIn: !previousState.isLoggedIn };
    });
  }
}

const styles = StyleSheet.create({
  headText: {
    textAlign: 'right',
    color: '#fff',
    fontSize: 20,
  },
  headStyle: {
    flex: 1,
    paddingTop: 20,
    paddingRight: 10,
    paddingBottom: 10,
    paddingLeft: 0,
    backgroundColor: '#35605a',
  },
});
