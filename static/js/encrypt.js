(async () => {
    const publicKeysArmored = [
        `-----BEGIN PGP PUBLIC KEY BLOCK-----
...
-----END PGP PUBLIC KEY BLOCK-----`,
        `-----BEGIN PGP PUBLIC KEY BLOCK-----
...
-----END PGP PUBLIC KEY BLOCK-----`
    ];
    const privateKeyArmored = `-----BEGIN PGP PRIVATE KEY BLOCK-----
...
-----END PGP PRIVATE KEY BLOCK-----`;    // encrypted private key
    const passphrase = `yourPassphrase`; // what the private key is encrypted with
    const message = 'Hello, World!';

    const { keys: [privateKey] } = await openpgp.key.readArmored(privateKeyArmored);
    await privateKey.decrypt(passphrase)

    const publicKeys = await Promise.all(publicKeysArmored.map(async (key) => {
        return (await openpgp.key.readArmored(key)).keys[0];
    }));

    const { data: encrypted } = await openpgp.encrypt({
        message: openpgp.message.fromText(message),   // input as Message object
        publicKeys,                                   // for encryption
        privateKeys: [privateKey]                     // for signing (optional)
    });
    console.log(encrypted); // '-----BEGIN PGP MESSAGE ... END PGP MESSAGE-----'
})();