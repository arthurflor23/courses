import React from 'react';
import { StackNavigator } from 'react-navigation';
import { Home } from './app/views/Home';
import { Contact } from './app/views/Contact';

const MyRoutes = StackNavigator({
  HomeRT: { screen: Home },
  ContactRT: { screen: Contact },
}, {
  initialRouteName: 'HomeRT',
});

export default class App extends React.Component {

  render() {
    return (
      <MyRoutes />
    );
  }

}
