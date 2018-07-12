import React from 'react';
import PropTypes from 'prop-types';

import {
  StyleSheet,
  Text,
  TextInput,
  View,
  TouchableHighlight,
} from 'react-native';

import {
  ALABASTER,
  ALTO_1,
  CERULEAN_1,
  DOVE_GRAY_1,
  WILD_SAND_1,
} from './colors';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-start',
    paddingTop: 150,
    backgroundColor: WILD_SAND_1,
  },
  input: {
    borderWidth: 1,
    borderColor: ALTO_1,
    height: 50,
    marginLeft: 10,
    marginRight: 10,
    padding: 15,
    borderRadius: 3,
  },
  buttonText: {
    fontSize: 18,
    fontWeight: '600',
    color: ALABASTER,
  },
  button: {
    height: 45,
    alignSelf: 'stretch',
    backgroundColor: CERULEAN_1,
    marginTop: 10,
    marginRight: 10,
    marginLeft: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  cancelButton: {
    backgroundColor: DOVE_GRAY_1,
  },
});

class TaskForm extends React.Component {
  onChangeText = (text) => {
    this.task = text;
  }

  onAddPressed = () => {
    this.props.onAdd(this.task);
  }

  render() {
    return (
      <View style={styles.container}>
        <TextInput
          style={styles.input}
          onChangeText={this.onChangeText}
        />
        <TouchableHighlight
          style={styles.button}
          onPress={this.onAddPressed}
        >
          <Text style={styles.buttonText}>Add</Text>
        </TouchableHighlight>
        <TouchableHighlight
          style={[styles.button, styles.cancelButton]}
          onPress={this.props.onCancel}
        >
          <Text style={styles.buttonText}>Cancel</Text>
        </TouchableHighlight>
      </View>
    );
  }
}

TaskForm.propTypes = {
  onCancel: PropTypes.func.isRequired,
  onAdd: PropTypes.func.isRequired,
};

export default TaskForm;
