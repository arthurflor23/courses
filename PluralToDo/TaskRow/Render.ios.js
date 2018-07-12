import React from 'react';
import {StyleSheet, Text, View} from 'react-native';

import Swipeout from 'react-native-swipeout';

import {CERULEAN_1, OUTER_SPACE_1, WHITE} from '../colors';

const localStyles = StyleSheet.create({
    container: {
        marginBottom: 20
    },
    row: {
        marginRight: 0,
        marginBottom: 0,
        marginLeft: 0
    }
});

export default function (baseStyles) {
    const buttons = [
        {
            text: 'Done',
            backgroundColor: CERULEAN_1,
            underlayColor: OUTER_SPACE_1,
            onPress: this.onDonePressed
        }
    ];
    return (
        <View style={localStyles.container}>
            <Swipeout backgroundColor={WHITE} right={buttons}>
                <View style={[baseStyles.container, localStyles.row]}>
                    <Text style={baseStyles.label}>{this.props.todo.task}</Text>
                </View>
            </Swipeout>
        </View>
    );
}
