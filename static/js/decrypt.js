//https://github.com/openpgpjs/openpgpjs/blob/master/README.md
<script src="static/js/openpgp.min.js"></script>
    <script>
(async () => {
    await openpgp.initWorker({ path: 'static/js/openpgp.worker.js' }); // set the relative web worker path

    // put keys in backtick (``) to avoid errors caused by spaces or tabs

        const publicKeyArmored = `-----BEGIN PGP PUBLIC KEY BLOCK-----

mI0EXja23gEEAKkkPrpu++xzk0I10lxz1TL+3iJUkAFErv8ayAGHpC78DCc30pcS
jfKZp9oRJdl9jUB95JGbFb5uuNBdQicwvWtXtjjPnsm67Z57asDuKpIz8olF22sB
G6KaFYJiIkCIfCndfkQDDxorQBZt0cwm0nvmQPgSquu4Hi7pEoOGQwO9ABEBAAG0
HW1hY2llayA8Y3phcm55QGN6YXJueS1sYXB0b3A+iM4EEwEKADgWIQR+obOZanzY
KKFB4Jt/feHJz/ZJ2AUCXja23gIbLwULCQgHAgYVCgkICwIEFgIDAQIeAQIXgAAK
CRB/feHJz/ZJ2FYIA/9OaBDgW9VORyQmG4FCs6V9k1IfI4ZGme5I0EpfBh/u4mYH
YUdNCiTxLoh468rtSbuT/0a5HbdBBn0jDi/ZdTu6IZtV9/UyzB6Mpb3udWHvnfMc
Hwyap17h3L5quXjwkUqdk6eeT0Cl4x0mbwmz+2DLXRZavvmoDW6DUPsx7Fkl9Q==
=l2ul
-----END PGP PUBLIC KEY BLOCK-----`;
        const privateKeyArmored = `-----BEGIN PGP PRIVATE KEY BLOCK-----

lQIGBF42tt4BBACpJD66bvvsc5NCNdJcc9Uy/t4iVJABRK7/GsgBh6Qu/AwnN9KX
Eo3ymafaESXZfY1AfeSRmxW+brjQXUInML1rV7Y4z57Juu2ee2rA7iqSM/KJRdtr
ARuimhWCYiJAiHwp3X5EAw8aK0AWbdHMJtJ75kD4EqrruB4u6RKDhkMDvQARAQAB
/gcDAlS/FcU44Gvk+qFOFYQIw6x7dgmBsSwzqEamGi8FBj3Xeps/6nGH42ankWPY
N47uqjgL0A+ggu9hhgbh0jWrVg6vQ6Ddir+Y6cGayx/KWgmjldpAvZ9p4KZeQkDJ
9M3wYwLlM2zpwUt/cxTLlqrpr7Qp7nQgzdqHjinGJNlroqYDkCK0oxhgmNXhMaf8
SiSyb7yMFkfQ/F+sprDylL+pEHLx69MwBNW5AxY0qC4ozZLg6XD4gCRO6mCT+hVh
Fut9uPTwQH6bfsAcno0fEgpi83Ho45K3Ot4G5M7j7/KZ7FWHWgSEXfGnSz9a8Lz2
KpMoEnG9nor59adGlHRfq1lmnP9tllBQF5s1XkFLOIJCKuU28O6eLSB8MkQIAPth
Uin5ApDPHA9ZPYJJNNbsJZ3T3gFciBj/9MuANfjjKoliLHG52Pfl/G+RhpAEhM1Y
/sRfvm8f/lALHWllJZRs84OKUcfOB+QFts4xa6Uz6rxg/azWVaDg4U60HW1hY2ll
ayA8Y3phcm55QGN6YXJueS1sYXB0b3A+iM4EEwEKADgWIQR+obOZanzYKKFB4Jt/
feHJz/ZJ2AUCXja23gIbLwULCQgHAgYVCgkICwIEFgIDAQIeAQIXgAAKCRB/feHJ
z/ZJ2FYIA/9OaBDgW9VORyQmG4FCs6V9k1IfI4ZGme5I0EpfBh/u4mYHYUdNCiTx
Loh468rtSbuT/0a5HbdBBn0jDi/ZdTu6IZtV9/UyzB6Mpb3udWHvnfMcHwyap17h
3L5quXjwkUqdk6eeT0Cl4x0mbwmz+2DLXRZavvmoDW6DUPsx7Fkl9Q==
=nUqD
-----END PGP PRIVATE KEY BLOCK-----`; // encrypted private key
        const passphrase = `sekret`; // what the private key is encrypted with

    const { keys: [privateKey] } = await openpgp.key.readArmored(privateKeyArmored);
    await privateKey.decrypt(passphrase);

<!--    const { data: encrypted } = await openpgp.encrypt({-->
<!--        message: openpgp.message.fromText('Hello, World!'),                 // input as Message object-->
<!--        publicKeys: (await openpgp.key.readArmored(publicKeyArmored)).keys, // for encryption-->
<!--        privateKeys: [privateKey]                                           // for signing (optional)-->
<!--    });-->
    const encrypted  =`-----BEGIN PGP MESSAGE-----

hIwDf33hyc/2SdgBA/4rTuH4738bjBZlMXGTx1LOdFnxPBuyL9DLewojeTAfzrsL
qTrPrATP/AFtoOAY5Jfz/4XyphPdrQSvhlD+43rq6OfO38ybpbd8/yzRTqrrARuL
vwsHlMG/G3g6g3aqmPo1IwyXH0XgAeijJKAFfGjfUKlEvRgCOHeFmvkcQqrSAtJG
ATBvpBZq+sq5TLqKK/u5pIwHMjnvqijAyc+qKm8psA1HIc74dpmIlGIVXFrL8KdU
V0A8H057aE8QFhL4SJi6PqZLwfBNVQ==
=tO9Z
-----END PGP MESSAGE-----`;


    console.log(encrypted); // '-----BEGIN PGP MESSAGE ... END PGP MESSAGE-----'
    const { data: decrypted } = await openpgp.decrypt({
        message: await openpgp.message.readArmored(encrypted),              // parse armored message
        publicKeys: (await openpgp.key.readArmored(publicKeyArmored)).keys, // for verification (optional)
        privateKeys: [privateKey]                                           // for decryption
    });
    console.log(decrypted); // 'Hello, World!'
    alert(decrypted);
})();

  </script>
