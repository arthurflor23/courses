// TODO: update deprecated component see https://facebook.github.io/react-native/docs/navigation.html}
import React from 'react';
import { Navigator } from 'react-native-deprecated-custom-components';
import TaskList from './TaskList';
import TaskForm from './TaskForm';
import store from './todoStore';

export default class PluralTodo extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.state = store.getState();

    store.subscribe((() => {
      this.setState(store.getState());
    }));

    this.onCancel = this.onCancel.bind(this);
    this.onAdd = this.onAdd.bind(this);
    this.onAddStarted = this.onAddStarted.bind(this);
    this.renderScene = this.renderScene.bind(this);
  }

  onAddStarted() {
    this.nav.push({
      name: 'taskform',
    });
  }

  onCancel() {
    this.nav.pop();
  }

  onAdd(task) {
    store.dispatch({
      type: 'ADD_TODO',
      task,
    });
    this.nav.pop();
  }

  onDone = (todo) => {
    store.dispatch({
      type: 'DONE_TODO',
      todo,
    });
  }

  onToggle = () => {
    store.dispatch({
      type: 'TOGGLE_STATE',
    });
  }

  configureScene() { // eslint-disable-line
    return Navigator.SceneConfigs.FloatFromBottom;
  }

  renderScene(route) {
    switch (route.name) {
      case 'taskform': {
        return (
          <TaskForm
            onCancel={this.onCancel}
            onAdd={this.onAdd}
          />
        );
      }
      default:
        return (
          <TaskList
            filter={this.state.filter}
            onAddStarted={this.onAddStarted}
            onDone={this.onDone}
            onToggle={this.onToggle}
            todos={this.state.todos}
          />
        );
    }
  }

  render() {
    return (
      <Navigator
        ref={((nav) => { this.nav = nav; })}
        configureScene={this.configureScene}
        initialRoute={{ name: 'tasklist', index: 0 }}
        renderScene={this.renderScene}
      />
    );
  }
}
