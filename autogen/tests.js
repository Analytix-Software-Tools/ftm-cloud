const fs = require('fs')

/**
 * Copies test cases by analyzing files in autogen/server/tests, separating their domain,
 * then copying the tests stubs (if they do not exist already) into the domains/DOM_NAME/test
 * folder.
 */
const copyTestSuites = () => {
    console.log('Copying test cases...')
    fs.readdir('./server/release/tests', (err, files) => {
        for (let i=0; i < files.length; i++) {
            const destinationDomain = files[i].split('_')[1]
            try {
                fs.readdir('../domains/' + destinationDomain + '/tests', (err, files) => {
                    if (files && !files.includes(`test_${destinationDomain}_api.py`)) {
                        fs.copyFile(`./server/release/tests/test_${destinationDomain}_api.py`, `../domains/${destinationDomain}/tests/test_${destinationDomain}_api.py`, (err) => {
                            if (err) console.error(err)
                            else console.log(`Test case for ${destinationDomain} allocated and transferred successfully.`);
                        });
                    } else {
                        console.error('Test case already defined or does not exist for domain ' + destinationDomain + '. Skipping test case transfer...')
                    }
                })
            } catch (error) {
                console.error('Domain not found: ' + destinationDomain + '. Skipping test case transfer...')
            }
        }
    })
}

copyTestSuites();