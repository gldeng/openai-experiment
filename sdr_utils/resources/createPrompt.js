var quantumStateMapping = {
 'Dead': 'a quantum state embodying the concept of \'Dead Cat,\' exploring the duality of existence where quantum uncertainties merge with the tranquility of a resting feline spirit.',
 'Alive': "a quantum state under the theme 'Alive Cat,' capturing the dynamic energy and playfulness resonating within the quantum realm and bringing the essence of life to the forefront.",
 'Gold': 'a quantum state infused with the essence of gold, blending the classical elegance of metal with the mysterious realms of quantum particles.',
 'Silver': 'a quantum state resonating with the brilliance of silver, reflecting the essence of both the physical and the quantum.',
 'Wood': 'a quantum state intertwined with the organic warmth of wood, merging the timeless essence of nature with the cutting-edge concepts of quantum mechanics.',
 'Water': 'a quantum state inspired by the element of water, where quantum waves dance in harmony with liquid dynamics.',
 'Fire': 'a quantum state ablaze with the intensity of fire, symbolizing the dynamic and transformative nature of quantum phenomena.',
 'Earth': 'a quantum state rooted in the stability and grounded energy of the earth, capturing the essence of solidity and foundation within the quantum realm.',
 'Air': 'a quantum state infused with the lightness and freedom of air, where quantum particles dance in the invisible currents of possibility.',
 'Metal': 'a quantum state resonating with the strength and conductivity of metal, embodying the fusion of classical durability with quantum complexity.',
 'Ice': 'a quantum state encapsulated in the crystalline elegance of ice, conveying the delicate balance between frozen stability and the quantum uncertainty.',
 'Lightning': 'a quantum state charged with the intensity of lightning, symbolizing the sudden and powerful transitions inherent in quantum systems.'
}

function _extractQuantumStateGroup(traitType, value) {
    var isThisGroup = ['quantumstate'].includes(traitType.toLowerCase().trim());
    if (!isThisGroup) {
        return null
    }
    var newValue = quantumStateMapping[value];
    if (!newValue) {
        newValue = 'a' + value + ' quantum state';
    }
    return {
        traitType: traitType,
        value: value,
        group: 'quantumstate',
        extracted: newValue
    };
}

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
    var isPetGroup = ['pet', 'pets'].includes(traitType.toLowerCase().trim());
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

function _extractHasGroup(traitType, value) {
    var isThisGroup = ['eyes', 'face', 'mouth', 'mustache', 'mustaches', 'paws', 'tails', 'tail', 'wings'].includes(traitType.toLowerCase().trim());
    if (!isThisGroup) {
        return null
    }
    var needsTraitType = !value.toLowerCase().includes(traitType.toLowerCase());
    var newValue = needsTraitType ? value + ' ' + traitType : value;
    return {
        traitType: traitType,
        value: value,
        group: 'has',
        extracted: newValue
    };
}


function _extractWearingGroup(traitType, value) {
    var isThisGroup = ['belt', 'belts', 'cap', 'hat', 'clothes', 'necklace', 'shoes', 'trousers', 'pants'].includes(traitType.toLowerCase().trim());
    if (!isThisGroup) {
        return null
    }
    return {
        traitType: traitType,
        value: value,
        group: 'wearing',
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


function _extractWeaponLeftGroup(traitType, value) {
    var isThisGroup = ['weaponleft'].includes(traitType.toLowerCase().trim());
    if (!isThisGroup) {
        return null
    }
    return {
        traitType: traitType,
        value: value,
        group: 'weaponleft',
        extracted: value.trim()
    };
}


function _extractWeaponRightGroup(traitType, value) {
    var isThisGroup = ['weaponright'].includes(traitType.toLowerCase().trim());
    if (!isThisGroup) {
        return null
    }
    return {
        traitType: traitType,
        value: value,
        group: 'weaponright',
        extracted: value.trim()
    };
}


function _extractAccessoryLeftGroup(traitType, value) {
    var isThisGroup = ['accessoryleft'].includes(traitType.toLowerCase().trim());
    if (!isThisGroup) {
        return null
    }
    return {
        traitType: traitType,
        value: value,
        group: 'accessoryleft',
        extracted: value.trim()
    };
}


function _extractAccessoryRightGroup(traitType, value) {
    var isThisGroup = ['accessoryright'].includes(traitType.toLowerCase().trim());
    if (!isThisGroup) {
        return null
    }
    return {
        traitType: traitType,
        value: value,
        group: 'accessoryright',
        extracted: value.trim()
    };
}

function _extractRideGroup(traitType, value) {
    var isThisGroup = ['ride', 'rides'].includes(traitType.toLowerCase().trim());
    if (!isThisGroup) {
        return null
    }
    return {
        traitType: traitType,
        value: value,
        group: 'ride',
        extracted: value.trim()
    };
}


function _extractZodiacGroup(traitType, value) {
    var isThisGroup = ['zodiac', 'zodiac sign', 'zodiac signs'].includes(traitType.toLowerCase().trim());
    if (!isThisGroup) {
        return null
    }
    var newValue = 'There is a badge on the top right corner, with the corresponding ' + value + ' zodiac image on it.';

    return {
        traitType: traitType,
        value: value,
        group: 'zodiac',
        extracted: newValue
    };
}

function _extract(trait_arg) {
    var handlers = [
        _extractQuantumStateGroup, _extractRideGroup,
        _extractBreedGroup, _extractBackgroundGroup, _extractPetGroup, _extractIsGroup, _extractHasGroup, _extractWearingGroup, _extractZodiacGroup, _extractAccessoryLeftGroup, _extractAccessoryRightGroup, _extractWeaponLeftGroup, _extractWeaponRightGroup, _extractWithGroup
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
    var groupQuantumState = _formatGroup(groups, 'quantumstate');
    var groupBreed = _formatGroup(groups, 'breed');
    var groupIs = _formatGroup(groups, 'is');
    var groupHas = _formatGroup(groups, 'has');
    var groupWearing = _formatGroup(groups, 'wearing');
    var groupZodiac = _formatGroup(groups, 'zodiac');
    var groupAccessoryLeft = _formatGroup(groups, 'accessoryleft');
    var groupAccessoryRight = _formatGroup(groups, 'accessoryright');
    var groupWeaponLeft = _formatGroup(groups, 'weaponleft');
    var groupWeaponRight = _formatGroup(groups, 'weaponright');
    var groupRide = _formatGroup(groups, 'ride');
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

    if (groupHas) {
        prompt = prompt + ' The main character has '+ groupHas + '.'
    }

    if (groupWearing) {
        prompt = prompt + ' The main character is wearing '+ groupWearing + '.'
    }

    if (groupWeaponLeft) {
        prompt = prompt + ' The main character is holding ' + groupWeaponLeft + ' in the left hand.'
    }

    if (groupWeaponRight) {
        prompt = prompt + ' The main character is holding ' + groupWeaponRight + ' in the right hand.'
    }

    if (groupAccessoryLeft) {
        prompt = prompt + ' The main character is wearing ' + groupAccessoryRight + ' on the left hand.'
    }

    if (groupAccessoryRight) {
        prompt = prompt + ' The main character is wearing ' + groupAccessoryRight + ' on the right hand.'
    }

    if (groupRide) {
        prompt = prompt + ' The main character is riding ' + groupRide + '.'
    }

    var groupPet = _formatGroup(groups, 'pet');
    if (groupPet != '') {
        prompt = prompt + ' It is accompanied by a pet ' + groupPet + '.'
    }

    if(groupZodiac) {
        prompt = prompt + ' ' + groupZodiac;
    }
    if(groupQuantumState) {
        prompt = prompt + ' The main character has ' + groupQuantumState + '.';
    }
    var groupBackground = _formatGroup(groups, 'background')
    if (groupBackground != '') {
        prompt = prompt + ' The image has a ' + groupBackground + ' background.'

    } else {
        ' The image has a solid background.'
    }
    prompt = prompt + ' The image should contain the full-body shot of the main character.'
    prompt = prompt + ' The image should contain one and only one cat.'
    prompt = prompt + ' The generated image should not contain any text or labels.'
    return prompt;
}
