import React from 'react';
import PropTypes from 'prop-types';
import {
  ListView,
  StyleSheet,
  Switch,
  Text,
  TouchableHighlight,
  View,
} from 'react-native';

import TaskRow from './TaskRow/Component';

import {
  ALABASTER,
  CERULEAN_1,
  WILD_SAND_1,
  MINE_SHAFT_1,
} from './colors';

const styles = StyleSheet.create({
  container: {
    paddingTop: 40,
    backgroundColor: WILD_SAND_1,
    flex: 1,
    justifyContent: 'flex-start',
  },
  button: {
    height: 60,
    borderColor: CERULEAN_1,
    borderWidth: 2,
    backgroundColor: MINE_SHAFT_1,
    margin: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonText: {
    color: ALABASTER,
    fontSize: 20,
    fontWeight: '600',
  },
  toggleRow: {
    flexDirection: 'row',
    padding: 10,
  },
  toggleText: {
    fontSize: 20,
    paddingLeft: 10,
    paddingTop: 3,
  },
});

class TaskList extends React.Component {
  constructor(props, context) {
    super(props, context);

    const dataSource = new ListView.DataSource({
      rowHasChanged: (r1, r2) => r1 !== r2,
    });

    this.state = {
      dataSource: dataSource.cloneWithRows(props.todos),
    };
  }

  componentWillReceiveProps(nextProps) {
    const dataSource = this
      .state
      .dataSource
      .cloneWithRows(nextProps.todos);

    this.setState({ dataSource });
  }

  renderRow = todo =>
    (<TaskRow
      onDone={this.props.onDone}
      todo={todo}
    />);


  render() {
    return (
      <View style={styles.container}>
        <View
          style={styles.toggleRow}
        >
          <Switch
            onValueChange={this.props.onToggle}
            style={styles.switch}
            value={this.props.filter !== 'pending'}
          />
          <Text
            style={styles.toggleText}
          >
            Showing {this.props.todos.length} {this.props.filter} todo(s)
          </Text>
        </View>
        <ListView
          key={this.props.todos}
          dataSource={this.state.dataSource}
          renderRow={this.renderRow}
          enableEmptySections
        />
        <TouchableHighlight
          onPress={this.props.onAddStarted}
          style={styles.button}
        >
          <Text style={styles.buttonText}>Add one</Text>
        </TouchableHighlight>
      </View>
    );
  }
}

TaskList.propTypes = {
  filter: PropTypes.string.isRequired,
  onAddStarted: PropTypes.func.isRequired,
  onDone: PropTypes.func.isRequired,
  onToggle: PropTypes.func.isRequired,
  todos: PropTypes.arrayOf(PropTypes.object).isRequired,
};

export default TaskList;
