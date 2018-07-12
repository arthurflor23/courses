import React from 'react';
import { StackNavigator } from 'react-navigation';
import EventList from './app/components/Event/EventList';
import EventForm from './app/components/Event/EventForm';

const MyRoutes = StackNavigator({
  list: {
    screen: EventList,
    navigationOptions: () => ({
      title: 'Your events',
    }),
  },
  form: {
    screen: EventForm,
    navigationOptions: () => ({
      title: 'Add an event',
    }),
  },
}, {
  initialRouteName: 'list',
});

export default class App extends React.Component {
  render() {
    return (<MyRoutes />);
  }
}
