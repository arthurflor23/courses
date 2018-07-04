import React from 'react';
import { StyleSheet, Image } from 'react-native';

export class Logo extends React.Component {
  render() {
    return (
      <Image source={ require('./img/office.jpg') } style={styles.logoImg}></Image>
    );
  }
}

const styles = StyleSheet.create({
  logoImg: {
    flex: 8,
    width: undefined,
    height: undefined,
  },
});
