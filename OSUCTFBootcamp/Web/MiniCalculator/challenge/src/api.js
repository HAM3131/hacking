const express = require('express')
const router = express.Router()
const Util = require('./util')

router.get('/calc/:expression', (req, res) => {
  try {
    Util.eval(req.params.expression)
      .then(result => res.status(200).send({ result: result }))
      .catch(err => res.status(400).send({ error: err.message }))
  } catch (e) {
    console.error(e)
    res.status(400).send(JSON.stringify(e))
  }
})

module.exports = router
