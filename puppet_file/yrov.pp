#ensure that ssh package is present
package{'ssh':
    ensure => present
}

package{'xterm':
    ensure => present
}

package{'python3':
    ensure => present
}

package{'htop':
    ensure => present
}