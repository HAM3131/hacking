class Util {
  require (resource) {
    return new Promise((resolve, reject) => {
      try {
        const module = require(resource)
        return resolve(module)
      } catch (ex) {
        return reject(ex)
      }
    })
  }

  eval (expression) {
    return new Promise((resolve, reject) => {
      try {
        const str = `var _ans = ${expression}; return _ans;`
        const func = new Function(str)
        const ans = func.call(this)
        resolve(ans)
      } catch (ex) {
        reject(ex)
      }
    })
  }
}

const UTIL_INSTANCE = new Util()
module.exports = UTIL_INSTANCE
