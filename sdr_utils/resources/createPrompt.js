function _extractBreedGroup(traitType, value) {
    var isBreedGroup = traitType.toLowerCase().trim() == 'breed';
    if (isBreedGroup) {
        return {
            traitType: traitType,
            value: value,
            group: 'breed',
            extracted: value.trim()
        };
    } else {
        return null;
    }
}

function _extractPetGroup(traitType, value) {
    var isPetGroup = traitType.toLowerCase().trim() == 'pet';
    if (isPetGroup) {
        return {
            traitType: traitType,
            value: value,
            group: 'pet',
            extracted: value.trim()
        };
    } else {
        return null;
    }
}

function _extractBackgroundGroup(traitType, value) {
    var isBackgroundGroup = traitType.toLowerCase().trim() == 'background';
    if (isBackgroundGroup) {
        return {
            traitType: traitType,
            value: value,
            group: 'background',
            extracted: value.trim()
        };
    } else {
        return null;
    }
}

function _extractIsGroup(traitType, value) {
    // to cater to 'is white-eyed'
    var tokens = value.trim().split(' ');
    var matching_the_target_pattern = tokens.length == 2 && tokens[0] == 'is';
    if (matching_the_target_pattern) {
        return {
            traitType: traitType,
            value: value,
            group: 'is',
            extracted: tokens[tokens.length - 1].trim()
        };
    } else {
        return null;
    }
}

function _extractWithGroup(traitType, value) {
    // this is the default group
    return {
        traitType: traitType,
        value: value,
        group: 'with',
        extracted: value.trim().replace('wears', '')
            .replace('wearing', '')
            .replace('is wearing', '')
            .replace('has', '').
            replace('Wears', '')
            .replace('Wearing', '')
            .replace('Is Wearing', '')
            .replace('Has', '')
    };
}

function _extract(trait_arg) {
    var handlers = [
        _extractBreedGroup, _extractBackgroundGroup, _extractPetGroup, _extractIsGroup, _extractWithGroup
    ];
    for (let i = 0; i < handlers.length; i++) {
        var obj = handlers[i](trait_arg.traitType, trait_arg.value);
        if (obj != null) {
            return obj;
        }
    }
}

function _makeGroups(traits_identified) {
    return traits_identified.reduce((accumulator, currentItem) => {
        const g = currentItem.group;
        if (!accumulator[g]) {
            accumulator[g] = [];
        }
        accumulator[g].push(currentItem);
        return accumulator;
    }, {});
}

function _joinWithCommasAndAnd(values) {
    if (values.length === 0) {
        return '';
    } else if (values.length === 1) {
        return values[0];
    } else {
        const last = values.pop(); // Removes and returns the last element
        const joined = values.join(', ');
        return `${joined}, and ${last}`;
    }
}

function _formatGroup(groups, groupName) {
    if (!groups.hasOwnProperty(groupName)) {
        return '';
    }
    return _joinWithCommasAndAnd(groups[groupName].map(x => x.extracted));
}

function createPrompt(config, trait_args) {
    prompt = config.prefix;
    var traits_identified = trait_args.map(_extract);
    var groups = _makeGroups(traits_identified);
    var groupBreed = _formatGroup(groups, 'breed');
    var groupIs = _formatGroup(groups, 'is');
    var groupWith = _formatGroup(groups, 'with');
    if (groupBreed != '') {
        prompt = prompt.replace(/image of a [\w\s]*[Cc]at/, 'image of a ' + groupBreed + ' cat');
    }
    if (groupIs != '' && groupWith != '') {
        prompt = prompt + ' that is ' + groupIs + ' and with ' + groupWith + '.';
    } else if (groupIs != '') {
        prompt = prompt + ' that is ' + groupIs + '.'
    } else if (groupWith != '') {
        prompt = prompt + ' with ' + groupWith + '.'
    } else {
        prompt = prompt + '.'
    }
    var groupPet = _formatGroup(groups, 'pet');
    if (groupPet != '') {
        prompt = prompt + ' It is accompanied by a pet ' + groupPet + '.'
    }
    var groupBackground = _formatGroup(groups, 'background')
    if (groupBackground != '') {
        prompt = prompt + ' The image has a ' + groupBackground + ' background.'

    } else {
        ' The image has a solid background.'
    }
    return prompt;
}
