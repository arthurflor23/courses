import React from 'react';
import PropTypes from 'prop-types';
import {StyleSheet} from 'react-native';
import {GRAY, GRAY_1, WHITE} from '../colors';
import Render from './Render';

/* eslint-disable react-native/no-unused-styles */
const styles = StyleSheet.create({
    container: {
        backgroundColor: WHITE,
        borderWidth: 1,
        borderColor: GRAY,
        padding: 20,
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 20,
        marginLeft: 20,
        marginRight: 20
    },
    label: {
        fontSize: 20,
        fontWeight: '300'
    },
    buttonDone: {
        borderRadius: 5,
        backgroundColor: GRAY_1,
        padding: 5
    }
});
/* eslint-enable react-native/no-unused-styles */

class TaskRow extends React.Component {
    onDonePressed = () => {
        this
            .props
            .onDone(this.props.todo);
    }
    render() {
        return (Render.bind(this)(styles));
    }
}

TaskRow.propTypes = {
    onDone: PropTypes.func.isRequired,
    todo: PropTypes
        .shape({task: PropTypes.string.isRequired})
        .isRequired
};

export default TaskRow;
