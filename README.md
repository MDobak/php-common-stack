# PHP Common Stack

Docker images with cron, composer and supervisor included 💪

## Managing PHP extensions
This image is provided with several additional tools for managing PHP extensions. These
tools allows you to easily enable or disable PHP extensions and change their configuration even on running containers:
  * `docker-pcs-php-ext-config`: allows to edit configuration of php extension. This script automatically finds 
    correct configuration file for given extension. This tool can be used for adding, modifying and removing
    configuration values.
    ```
    # Adding and modifying:
    docker-pcs-php-ext-config opcache \
        opcache.memory_consumption=512 \
        opcache.interned_strings_buffer=8 \
        opcache.max_accelerated_files=10000 \
        opcache.revalidate_freq=0 \
        opcache.fast_shutdown=1 \
        opcache.enable_cli=1 \
        opcache.enable=1
    # Removing:
    docker-pcs-php-ext-config opcache \
        --rm opcache.memory_consumption \
        --rm opcache.interned_strings_buffer
    ```
    This tool can be also used for editing php.ini file:
    ```
    touch /usr/local/etc/php/php.ini # make sure this php.ini file exists
    docker-pcs-php-ext-config php --ini-name ../php.ini \
        log_errors=On \
        access_log=/dev/stdout \
        error_log=/dev/stderr
    ```
    Paths provided by the `ini-name` argument are relative to `/usr/local/etc/php/conf.d/` directory.
    
    On running containers you can also add `--restart` argument to automatically restart the PHP process.
  * `docker-pcs-php-ext-enable` and `docker-pcs-php-ext-disable`: similar to `phpenmod` and `phpdismod`. You
    can also use `--restart` argument as in `docker-pcs-php-ext-config` script.
  * `docker-pcs-php-ext-install`: works similar to `docker-php-ext-install` but fallback to `pecl` if extension source 
  isn't provided with image. This script also automatically enables installed extensions.
  * `docker-pcs-php-restart`: restarts FPM or Apache process to reload configuration. 

Detailed instruction how to install PHP extension you can find in [official PHP docker images documentation](https://hub.docker.com/_/php/). 

## Debugging container with XDebug

For your local development, you can create a separate `Dockerfile` with preinstalled XDebug:
```
FROM mdobak/php-common-stack:fpm-alpine

# your configuration

RUN    docker-pcs-php-ext-install xdebug \
    && docker-pcs-php-ext-config xdebug \
           xdebug.remote_enable=1 \
           xdebug.remote_autostart=1 \
           xdebug.remote_host=172.17.0.1
           #xdebug.remote_host=docker.for.mac.localhost

``` 
XDebug slows down PHP execution noticeably so most likely you won't want to keep it working on all the time. 
Fortunately, you can easily enable and disable XDebug using `docker-pcs-php-ext-enable` and `docker-pcs-php-ext-disable`
commands described earlier. You can use these commands by logging into container's root shell or with `docker exec` 
command, e.g: `docker exec CONTAINER_NAME docker-pcs-php-ext-disable xdebug`.

Alternatively, you can disable `xdebug.remote_autostart` and manage XDebug using cookies but this approach prevents you 
from debugging cron and supervisor scripts.

More information about XDebug you can find in [official documentation](https://xdebug.org/docs/remote).

## Adding custom crontabs

On Debian images a cron job can be defined in a crontab-like files in the `/etc/cron.d/` directory or added within the 
`/etc/crontab file`. On Alpine images you can use only crontab-like files in the `/etc/crontab/` directory.

## Adding custom supervisor program

To add a program, you’ll need to add the supervisord configuration file. For Debian based images configuration files 
should be stored in `/etc/supervisor/conf.d/` directory and for Alpine based images in  `/etc/supervisor.d/`. In both 
of these directories is defined default `supervisord.conf` file so be careful to not overwrite it. 

Simplest configuration file for supervisor can looks like this:
```
[program:my_app]
command = /var/www/html/bin/console my:worker
stdout_logfile = /dev/stdout
stdout_logfile_maxbytes = 0
stderr_logfile = /dev/stderr
stderr_logfile_maxbytes = 0
```

More information about Supervisord you can find in [official documentation](http://supervisord.org/).

## More?

This images are based on official PHP docker images and more details you can find [their documentation](https://hub.docker.com/_/php/).

## Supported tags and respective Dockerfile links

<!--- BEGIN_TAGS_LIST -->

  * fpm branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.fpm): `5.4-fpm`, `5.4.35-fpm`, `5.4.36-fpm`, `5.4.37-fpm`, `5.4.38-fpm`, `5.4.39-fpm`, `5.4.40-fpm`, `5.4.41-fpm`, `5.4.42-fpm`, `5.4.43-fpm`, `5.4.44-fpm`, `5.4.45-fpm`, `5.5-fpm`, `5.5.19-fpm`, `5.5.20-fpm`, `5.5.21-fpm`, `5.5.22-fpm`, `5.5.23-fpm`, `5.5.24-fpm`, `5.5.25-fpm`, `5.5.26-fpm`, `5.5.27-fpm`, `5.5.28-fpm`, `5.5.29-fpm`, `5.5.30-fpm`, `5.5.31-fpm`, `5.5.32-fpm`, `5.5.33-fpm`, `5.5.34-fpm`, `5.5.35-fpm`, `5.5.36-fpm`, `5.5.37-fpm`, `5.5.38-fpm`, `5.6-fpm`, `5.6.10-fpm`, `5.6.11-fpm`, `5.6.12-fpm`, `5.6.13-fpm`, `5.6.14-fpm`, `5.6.15-fpm`, `5.6.16-fpm`, `5.6.17-fpm`, `5.6.18-fpm`, `5.6.19-fpm`, `5.6.20-fpm`, `5.6.21-fpm`, `5.6.22-fpm`, `5.6.23-fpm`, `5.6.24-fpm`, `5.6.25-fpm`, `5.6.26-fpm`, `5.6.27-fpm`, `5.6.28-fpm`, `5.6.29-fpm`, `5.6.3-fpm`, `5.6.30-fpm`, `5.6.31-fpm`, `5.6.32-fpm`, `5.6.33-fpm`, `5.6.34-fpm`, `5.6.35-fpm`, `5.6.36-fpm`, `5.6.37-fpm`, `5.6.38-fpm`, `5.6.39-fpm`, `5.6.4-fpm`, `5.6.40-fpm`, `5.6.5-fpm`, `5.6.6-fpm`, `5.6.7-fpm`, `5.6.8-fpm`, `5.6.9-fpm`, `7.0-fpm`, `7.0.0-fpm`, `7.0.0RC1-fpm`, `7.0.0RC2-fpm`, `7.0.0RC3-fpm`, `7.0.0RC4-fpm`, `7.0.0RC5-fpm`, `7.0.0RC6-fpm`, `7.0.0RC7-fpm`, `7.0.0RC8-fpm`, `7.0.0beta1-fpm`, `7.0.0beta2-fpm`, `7.0.0beta3-fpm`, `7.0.1-fpm`, `7.0.10-fpm`, `7.0.11-fpm`, `7.0.12-fpm`, `7.0.13-fpm`, `7.0.14-fpm`, `7.0.15-fpm`, `7.0.16-fpm`, `7.0.17-fpm`, `7.0.18-fpm`, `7.0.19-fpm`, `7.0.2-fpm`, `7.0.20-fpm`, `7.0.21-fpm`, `7.0.22-fpm`, `7.0.23-fpm`, `7.0.24-fpm`, `7.0.25-fpm`, `7.0.26-fpm`, `7.0.27-fpm`, `7.0.28-fpm`, `7.0.29-fpm`, `7.0.3-fpm`, `7.0.30-fpm`, `7.0.31-fpm`, `7.0.32-fpm`, `7.0.33-fpm`, `7.0.4-fpm`, `7.0.5-fpm`, `7.0.6-fpm`, `7.0.7-fpm`, `7.0.8-fpm`, `7.0.9-fpm`, `7.1-fpm`, `7.1.0-fpm`, `7.1.0RC1-fpm`, `7.1.0RC2-fpm`, `7.1.0RC3-fpm`, `7.1.0RC4-fpm`, `7.1.0RC5-fpm`, `7.1.0RC6-fpm`, `7.1.1-fpm`, `7.1.10-fpm`, `7.1.11-fpm`, `7.1.12-fpm`, `7.1.13-fpm`, `7.1.14-fpm`, `7.1.15-fpm`, `7.1.16-fpm`, `7.1.17-fpm`, `7.1.18-fpm`, `7.1.19-fpm`, `7.1.2-fpm`, `7.1.20-fpm`, `7.1.21-fpm`, `7.1.22-fpm`, `7.1.23-fpm`, `7.1.24-fpm`, `7.1.25-fpm`, `7.1.26-fpm`, `7.1.27-fpm`, `7.1.28-fpm`, `7.1.29-fpm`, `7.1.3-fpm`, `7.1.30-fpm`, `7.1.31-fpm`, `7.1.4-fpm`, `7.1.5-fpm`, `7.1.6-fpm`, `7.1.7-fpm`, `7.1.8-fpm`, `7.1.9-fpm`, `7.2-fpm`, `7.2.0-fpm`, `7.2.0RC1-fpm`, `7.2.0RC2-fpm`, `7.2.0RC3-fpm`, `7.2.0RC4-fpm`, `7.2.0RC5-fpm`, `7.2.0RC6-fpm`, `7.2.0alpha3-fpm`, `7.2.0beta1-fpm`, `7.2.0beta2-fpm`, `7.2.0beta3-fpm`, `7.2.1-fpm`, `7.2.10-fpm`, `7.2.11-fpm`, `7.2.12-fpm`, `7.2.13-fpm`, `7.2.14-fpm`, `7.2.15-fpm`, `7.2.16-fpm`, `7.2.17-fpm`, `7.2.18-fpm`, `7.2.19-fpm`, `7.2.2-fpm`, `7.2.20-fpm`, `7.2.21-fpm`, `7.2.3-fpm`, `7.2.4-fpm`, `7.2.5-fpm`, `7.2.6-fpm`, `7.2.7-fpm`, `7.2.8-fpm`, `7.2.9-fpm`, `7.2edge-fpm`, `7.2unstable-fpm`, `7.3-fpm`, `7.3.0-fpm`, `7.3.0RC1-fpm`, `7.3.0RC2-fpm`, `7.3.0RC3-fpm`, `7.3.0RC4-fpm`, `7.3.0RC5-fpm`, `7.3.0RC6-fpm`, `7.3.0beta2-fpm`, `7.3.0beta3-fpm`, `7.3.1-fpm`, `7.3.2-fpm`, `7.3.3-fpm`, `7.3.4-fpm`, `7.3.5-fpm`, `7.3.6-fpm`, `7.3.7-fpm`, `7.3.8-fpm`, `7.3edge-fpm`, `7.3unstable-fpm`, `7.4.0alpha1-fpm`, `7.4.0alpha2-fpm`, `7.4.0alpha3-fpm`, `7.4.0beta1-fpm`, `7.4edge-fpm`, `7.4unstable-fpm`, `edge-fpm`, `latest-fpm`
  * apache branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.apache): `5.4-apache`, `5.4.36-apache`, `5.4.37-apache`, `5.4.38-apache`, `5.4.39-apache`, `5.4.40-apache`, `5.4.41-apache`, `5.4.42-apache`, `5.4.43-apache`, `5.4.44-apache`, `5.4.45-apache`, `5.5-apache`, `5.5.20-apache`, `5.5.21-apache`, `5.5.22-apache`, `5.5.23-apache`, `5.5.24-apache`, `5.5.25-apache`, `5.5.26-apache`, `5.5.27-apache`, `5.5.28-apache`, `5.5.29-apache`, `5.5.30-apache`, `5.5.31-apache`, `5.5.32-apache`, `5.5.33-apache`, `5.5.34-apache`, `5.5.35-apache`, `5.5.36-apache`, `5.5.37-apache`, `5.5.38-apache`, `5.6-apache`, `5.6.10-apache`, `5.6.11-apache`, `5.6.12-apache`, `5.6.13-apache`, `5.6.14-apache`, `5.6.15-apache`, `5.6.16-apache`, `5.6.17-apache`, `5.6.18-apache`, `5.6.19-apache`, `5.6.20-apache`, `5.6.21-apache`, `5.6.22-apache`, `5.6.23-apache`, `5.6.24-apache`, `5.6.25-apache`, `5.6.26-apache`, `5.6.27-apache`, `5.6.28-apache`, `5.6.29-apache`, `5.6.30-apache`, `5.6.31-apache`, `5.6.32-apache`, `5.6.33-apache`, `5.6.34-apache`, `5.6.35-apache`, `5.6.36-apache`, `5.6.37-apache`, `5.6.38-apache`, `5.6.39-apache`, `5.6.4-apache`, `5.6.40-apache`, `5.6.5-apache`, `5.6.6-apache`, `5.6.7-apache`, `5.6.8-apache`, `5.6.9-apache`, `7.0-apache`, `7.0.0-apache`, `7.0.0RC1-apache`, `7.0.0RC2-apache`, `7.0.0RC3-apache`, `7.0.0RC4-apache`, `7.0.0RC5-apache`, `7.0.0RC6-apache`, `7.0.0RC7-apache`, `7.0.0RC8-apache`, `7.0.0beta1-apache`, `7.0.0beta2-apache`, `7.0.0beta3-apache`, `7.0.1-apache`, `7.0.10-apache`, `7.0.11-apache`, `7.0.12-apache`, `7.0.13-apache`, `7.0.14-apache`, `7.0.15-apache`, `7.0.16-apache`, `7.0.17-apache`, `7.0.18-apache`, `7.0.19-apache`, `7.0.2-apache`, `7.0.20-apache`, `7.0.21-apache`, `7.0.22-apache`, `7.0.23-apache`, `7.0.24-apache`, `7.0.25-apache`, `7.0.26-apache`, `7.0.27-apache`, `7.0.28-apache`, `7.0.29-apache`, `7.0.3-apache`, `7.0.30-apache`, `7.0.31-apache`, `7.0.32-apache`, `7.0.33-apache`, `7.0.4-apache`, `7.0.5-apache`, `7.0.6-apache`, `7.0.7-apache`, `7.0.8-apache`, `7.0.9-apache`, `7.1-apache`, `7.1.0-apache`, `7.1.0RC1-apache`, `7.1.0RC2-apache`, `7.1.0RC3-apache`, `7.1.0RC4-apache`, `7.1.0RC5-apache`, `7.1.0RC6-apache`, `7.1.1-apache`, `7.1.10-apache`, `7.1.11-apache`, `7.1.12-apache`, `7.1.13-apache`, `7.1.14-apache`, `7.1.15-apache`, `7.1.16-apache`, `7.1.17-apache`, `7.1.18-apache`, `7.1.19-apache`, `7.1.2-apache`, `7.1.20-apache`, `7.1.21-apache`, `7.1.22-apache`, `7.1.23-apache`, `7.1.24-apache`, `7.1.25-apache`, `7.1.26-apache`, `7.1.27-apache`, `7.1.28-apache`, `7.1.29-apache`, `7.1.3-apache`, `7.1.30-apache`, `7.1.31-apache`, `7.1.4-apache`, `7.1.5-apache`, `7.1.6-apache`, `7.1.7-apache`, `7.1.8-apache`, `7.1.9-apache`, `7.2-apache`, `7.2.0-apache`, `7.2.0RC1-apache`, `7.2.0RC2-apache`, `7.2.0RC3-apache`, `7.2.0RC4-apache`, `7.2.0RC5-apache`, `7.2.0RC6-apache`, `7.2.0alpha3-apache`, `7.2.0beta1-apache`, `7.2.0beta2-apache`, `7.2.0beta3-apache`, `7.2.1-apache`, `7.2.10-apache`, `7.2.11-apache`, `7.2.12-apache`, `7.2.13-apache`, `7.2.14-apache`, `7.2.15-apache`, `7.2.16-apache`, `7.2.17-apache`, `7.2.18-apache`, `7.2.19-apache`, `7.2.2-apache`, `7.2.20-apache`, `7.2.21-apache`, `7.2.3-apache`, `7.2.4-apache`, `7.2.5-apache`, `7.2.6-apache`, `7.2.7-apache`, `7.2.8-apache`, `7.2.9-apache`, `7.2edge-apache`, `7.2unstable-apache`, `7.3-apache`, `7.3.0-apache`, `7.3.0RC1-apache`, `7.3.0RC2-apache`, `7.3.0RC3-apache`, `7.3.0RC4-apache`, `7.3.0RC5-apache`, `7.3.0RC6-apache`, `7.3.0beta2-apache`, `7.3.0beta3-apache`, `7.3.1-apache`, `7.3.2-apache`, `7.3.3-apache`, `7.3.4-apache`, `7.3.5-apache`, `7.3.6-apache`, `7.3.7-apache`, `7.3.8-apache`, `7.3edge-apache`, `7.3unstable-apache`, `7.4.0alpha1-apache`, `7.4.0alpha2-apache`, `7.4.0alpha3-apache`, `7.4.0beta1-apache`, `7.4edge-apache`, `7.4unstable-apache`, `edge-apache`, `latest-apache`
  * cli branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.cli): `5.4-cli`, `5.4.33-cli`, `5.4.35-cli`, `5.4.36-cli`, `5.4.37-cli`, `5.4.38-cli`, `5.4.39-cli`, `5.4.40-cli`, `5.4.41-cli`, `5.4.42-cli`, `5.4.43-cli`, `5.4.44-cli`, `5.4.45-cli`, `5.5-cli`, `5.5.17-cli`, `5.5.18-cli`, `5.5.19-cli`, `5.5.20-cli`, `5.5.21-cli`, `5.5.22-cli`, `5.5.23-cli`, `5.5.24-cli`, `5.5.25-cli`, `5.5.26-cli`, `5.5.27-cli`, `5.5.28-cli`, `5.5.29-cli`, `5.5.30-cli`, `5.5.31-cli`, `5.5.32-cli`, `5.5.33-cli`, `5.5.34-cli`, `5.5.35-cli`, `5.5.36-cli`, `5.5.37-cli`, `5.5.38-cli`, `5.6-cli`, `5.6.1-cli`, `5.6.10-cli`, `5.6.11-cli`, `5.6.12-cli`, `5.6.13-cli`, `5.6.14-cli`, `5.6.15-cli`, `5.6.16-cli`, `5.6.17-cli`, `5.6.18-cli`, `5.6.19-cli`, `5.6.2-cli`, `5.6.20-cli`, `5.6.21-cli`, `5.6.22-cli`, `5.6.23-cli`, `5.6.24-cli`, `5.6.25-cli`, `5.6.26-cli`, `5.6.27-cli`, `5.6.28-cli`, `5.6.29-cli`, `5.6.3-cli`, `5.6.30-cli`, `5.6.31-cli`, `5.6.32-cli`, `5.6.33-cli`, `5.6.34-cli`, `5.6.35-cli`, `5.6.36-cli`, `5.6.37-cli`, `5.6.38-cli`, `5.6.39-cli`, `5.6.4-cli`, `5.6.40-cli`, `5.6.5-cli`, `5.6.6-cli`, `5.6.7-cli`, `5.6.8-cli`, `5.6.9-cli`, `7.0-cli`, `7.0.0-cli`, `7.0.0RC1-cli`, `7.0.0RC2-cli`, `7.0.0RC3-cli`, `7.0.0RC4-cli`, `7.0.0RC5-cli`, `7.0.0RC6-cli`, `7.0.0RC7-cli`, `7.0.0RC8-cli`, `7.0.0beta1-cli`, `7.0.0beta2-cli`, `7.0.0beta3-cli`, `7.0.1-cli`, `7.0.10-cli`, `7.0.11-cli`, `7.0.12-cli`, `7.0.13-cli`, `7.0.14-cli`, `7.0.15-cli`, `7.0.16-cli`, `7.0.17-cli`, `7.0.18-cli`, `7.0.19-cli`, `7.0.2-cli`, `7.0.20-cli`, `7.0.21-cli`, `7.0.22-cli`, `7.0.23-cli`, `7.0.24-cli`, `7.0.25-cli`, `7.0.26-cli`, `7.0.27-cli`, `7.0.28-cli`, `7.0.29-cli`, `7.0.3-cli`, `7.0.30-cli`, `7.0.31-cli`, `7.0.32-cli`, `7.0.33-cli`, `7.0.4-cli`, `7.0.5-cli`, `7.0.6-cli`, `7.0.7-cli`, `7.0.8-cli`, `7.0.9-cli`, `7.1-cli`, `7.1.0-cli`, `7.1.0RC1-cli`, `7.1.0RC2-cli`, `7.1.0RC3-cli`, `7.1.0RC4-cli`, `7.1.0RC5-cli`, `7.1.0RC6-cli`, `7.1.1-cli`, `7.1.10-cli`, `7.1.11-cli`, `7.1.12-cli`, `7.1.13-cli`, `7.1.14-cli`, `7.1.15-cli`, `7.1.16-cli`, `7.1.17-cli`, `7.1.18-cli`, `7.1.19-cli`, `7.1.2-cli`, `7.1.20-cli`, `7.1.21-cli`, `7.1.22-cli`, `7.1.23-cli`, `7.1.24-cli`, `7.1.25-cli`, `7.1.26-cli`, `7.1.27-cli`, `7.1.28-cli`, `7.1.29-cli`, `7.1.3-cli`, `7.1.30-cli`, `7.1.31-cli`, `7.1.4-cli`, `7.1.5-cli`, `7.1.6-cli`, `7.1.7-cli`, `7.1.8-cli`, `7.1.9-cli`, `7.2-cli`, `7.2.0-cli`, `7.2.0RC1-cli`, `7.2.0RC2-cli`, `7.2.0RC3-cli`, `7.2.0RC4-cli`, `7.2.0RC5-cli`, `7.2.0RC6-cli`, `7.2.0alpha3-cli`, `7.2.0beta1-cli`, `7.2.0beta2-cli`, `7.2.0beta3-cli`, `7.2.1-cli`, `7.2.10-cli`, `7.2.11-cli`, `7.2.12-cli`, `7.2.13-cli`, `7.2.14-cli`, `7.2.15-cli`, `7.2.16-cli`, `7.2.17-cli`, `7.2.18-cli`, `7.2.19-cli`, `7.2.2-cli`, `7.2.20-cli`, `7.2.21-cli`, `7.2.3-cli`, `7.2.4-cli`, `7.2.5-cli`, `7.2.6-cli`, `7.2.7-cli`, `7.2.8-cli`, `7.2.9-cli`, `7.2edge-cli`, `7.2unstable-cli`, `7.3-cli`, `7.3.0-cli`, `7.3.0RC1-cli`, `7.3.0RC2-cli`, `7.3.0RC3-cli`, `7.3.0RC4-cli`, `7.3.0RC5-cli`, `7.3.0RC6-cli`, `7.3.0beta2-cli`, `7.3.0beta3-cli`, `7.3.1-cli`, `7.3.2-cli`, `7.3.3-cli`, `7.3.4-cli`, `7.3.5-cli`, `7.3.6-cli`, `7.3.7-cli`, `7.3.8-cli`, `7.3edge-cli`, `7.3unstable-cli`, `7.4.0alpha1-cli`, `7.4.0alpha2-cli`, `7.4.0alpha3-cli`, `7.4.0beta1-cli`, `7.4edge-cli`, `7.4unstable-cli`, `edge-cli`, `latest-cli`
  * fpm-jessie branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.fpm-jessie): `5.6-fpm-jessie`, `5.6.31-fpm-jessie`, `5.6.32-fpm-jessie`, `5.6.33-fpm-jessie`, `5.6.34-fpm-jessie`, `5.6.35-fpm-jessie`, `5.6.36-fpm-jessie`, `5.6.37-fpm-jessie`, `5.6.38-fpm-jessie`, `5.6.39-fpm-jessie`, `5.6.40-fpm-jessie`, `7.0-fpm-jessie`, `7.0.24-fpm-jessie`, `7.0.25-fpm-jessie`, `7.0.26-fpm-jessie`, `7.0.27-fpm-jessie`, `7.0.28-fpm-jessie`, `7.0.29-fpm-jessie`, `7.0.30-fpm-jessie`, `7.0.31-fpm-jessie`, `7.0.32-fpm-jessie`, `7.0.33-fpm-jessie`, `7.1-fpm-jessie`, `7.1.10-fpm-jessie`, `7.1.11-fpm-jessie`, `7.1.12-fpm-jessie`, `7.1.13-fpm-jessie`, `7.1.14-fpm-jessie`, `7.1.15-fpm-jessie`, `7.1.16-fpm-jessie`, `7.1.17-fpm-jessie`, `7.1.18-fpm-jessie`, `7.1.19-fpm-jessie`, `7.1.20-fpm-jessie`, `7.1.21-fpm-jessie`, `7.1.22-fpm-jessie`, `7.1.23-fpm-jessie`, `7.1.24-fpm-jessie`, `7.1.25-fpm-jessie`, `7.1.26-fpm-jessie`, `7.1.27-fpm-jessie`, `7.1.28-fpm-jessie`, `7.1.29-fpm-jessie`, `7.1.30-fpm-jessie`, `7.1edge-fpm-jessie`, `7.1unstable-fpm-jessie`, `edge-fpm-jessie`, `latest-fpm-jessie`
  * apache-jessie branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.apache-jessie): `5.6-apache-jessie`, `5.6.31-apache-jessie`, `5.6.32-apache-jessie`, `5.6.33-apache-jessie`, `5.6.34-apache-jessie`, `5.6.35-apache-jessie`, `5.6.36-apache-jessie`, `5.6.37-apache-jessie`, `5.6.38-apache-jessie`, `5.6.39-apache-jessie`, `5.6.40-apache-jessie`, `7.0-apache-jessie`, `7.0.24-apache-jessie`, `7.0.25-apache-jessie`, `7.0.26-apache-jessie`, `7.0.27-apache-jessie`, `7.0.28-apache-jessie`, `7.0.29-apache-jessie`, `7.0.30-apache-jessie`, `7.0.31-apache-jessie`, `7.0.32-apache-jessie`, `7.0.33-apache-jessie`, `7.1-apache-jessie`, `7.1.10-apache-jessie`, `7.1.11-apache-jessie`, `7.1.12-apache-jessie`, `7.1.13-apache-jessie`, `7.1.14-apache-jessie`, `7.1.15-apache-jessie`, `7.1.16-apache-jessie`, `7.1.17-apache-jessie`, `7.1.18-apache-jessie`, `7.1.19-apache-jessie`, `7.1.20-apache-jessie`, `7.1.21-apache-jessie`, `7.1.22-apache-jessie`, `7.1.23-apache-jessie`, `7.1.24-apache-jessie`, `7.1.25-apache-jessie`, `7.1.26-apache-jessie`, `7.1.27-apache-jessie`, `7.1.28-apache-jessie`, `7.1.29-apache-jessie`, `7.1.30-apache-jessie`, `7.1edge-apache-jessie`, `7.1unstable-apache-jessie`, `edge-apache-jessie`, `latest-apache-jessie`
  * cli-jessie branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.cli-jessie): `5.6-cli-jessie`, `5.6.31-cli-jessie`, `5.6.32-cli-jessie`, `5.6.33-cli-jessie`, `5.6.34-cli-jessie`, `5.6.35-cli-jessie`, `5.6.36-cli-jessie`, `5.6.37-cli-jessie`, `5.6.38-cli-jessie`, `5.6.39-cli-jessie`, `5.6.40-cli-jessie`, `7.0-cli-jessie`, `7.0.24-cli-jessie`, `7.0.25-cli-jessie`, `7.0.26-cli-jessie`, `7.0.27-cli-jessie`, `7.0.28-cli-jessie`, `7.0.29-cli-jessie`, `7.0.30-cli-jessie`, `7.0.31-cli-jessie`, `7.0.32-cli-jessie`, `7.0.33-cli-jessie`, `7.1-cli-jessie`, `7.1.10-cli-jessie`, `7.1.11-cli-jessie`, `7.1.12-cli-jessie`, `7.1.13-cli-jessie`, `7.1.14-cli-jessie`, `7.1.15-cli-jessie`, `7.1.16-cli-jessie`, `7.1.17-cli-jessie`, `7.1.18-cli-jessie`, `7.1.19-cli-jessie`, `7.1.20-cli-jessie`, `7.1.21-cli-jessie`, `7.1.22-cli-jessie`, `7.1.23-cli-jessie`, `7.1.24-cli-jessie`, `7.1.25-cli-jessie`, `7.1.26-cli-jessie`, `7.1.27-cli-jessie`, `7.1.28-cli-jessie`, `7.1.29-cli-jessie`, `7.1.30-cli-jessie`, `7.1edge-cli-jessie`, `edge-cli-jessie`, `latest-cli-jessie`
  * fpm-stretch branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.fpm-stretch): `5.6-fpm-stretch`, `5.6.36-fpm-stretch`, `5.6.37-fpm-stretch`, `5.6.38-fpm-stretch`, `5.6.39-fpm-stretch`, `5.6.40-fpm-stretch`, `7.0-fpm-stretch`, `7.0.30-fpm-stretch`, `7.0.31-fpm-stretch`, `7.0.32-fpm-stretch`, `7.0.33-fpm-stretch`, `7.1-fpm-stretch`, `7.1.17-fpm-stretch`, `7.1.18-fpm-stretch`, `7.1.19-fpm-stretch`, `7.1.20-fpm-stretch`, `7.1.21-fpm-stretch`, `7.1.22-fpm-stretch`, `7.1.23-fpm-stretch`, `7.1.24-fpm-stretch`, `7.1.25-fpm-stretch`, `7.1.26-fpm-stretch`, `7.1.27-fpm-stretch`, `7.1.28-fpm-stretch`, `7.1.29-fpm-stretch`, `7.1.30-fpm-stretch`, `7.1.31-fpm-stretch`, `7.2-fpm-stretch`, `7.2.0-fpm-stretch`, `7.2.0RC4-fpm-stretch`, `7.2.0RC5-fpm-stretch`, `7.2.0RC6-fpm-stretch`, `7.2.1-fpm-stretch`, `7.2.10-fpm-stretch`, `7.2.11-fpm-stretch`, `7.2.12-fpm-stretch`, `7.2.13-fpm-stretch`, `7.2.14-fpm-stretch`, `7.2.15-fpm-stretch`, `7.2.16-fpm-stretch`, `7.2.17-fpm-stretch`, `7.2.18-fpm-stretch`, `7.2.19-fpm-stretch`, `7.2.2-fpm-stretch`, `7.2.20-fpm-stretch`, `7.2.21-fpm-stretch`, `7.2.3-fpm-stretch`, `7.2.4-fpm-stretch`, `7.2.5-fpm-stretch`, `7.2.6-fpm-stretch`, `7.2.7-fpm-stretch`, `7.2.8-fpm-stretch`, `7.2.9-fpm-stretch`, `7.2edge-fpm-stretch`, `7.2unstable-fpm-stretch`, `7.3-fpm-stretch`, `7.3.0-fpm-stretch`, `7.3.0RC1-fpm-stretch`, `7.3.0RC2-fpm-stretch`, `7.3.0RC3-fpm-stretch`, `7.3.0RC4-fpm-stretch`, `7.3.0RC5-fpm-stretch`, `7.3.0RC6-fpm-stretch`, `7.3.0beta2-fpm-stretch`, `7.3.0beta3-fpm-stretch`, `7.3.1-fpm-stretch`, `7.3.2-fpm-stretch`, `7.3.3-fpm-stretch`, `7.3.4-fpm-stretch`, `7.3.5-fpm-stretch`, `7.3.6-fpm-stretch`, `7.3.7-fpm-stretch`, `7.3.8-fpm-stretch`, `7.3edge-fpm-stretch`, `7.3unstable-fpm-stretch`, `7.4.0alpha1-fpm-stretch`, `7.4.0alpha2-fpm-stretch`, `7.4edge-fpm-stretch`, `7.4unstable-fpm-stretch`, `edge-fpm-stretch`, `latest-fpm-stretch`
  * apache-stretch branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.apache-stretch): `5.6-apache-stretch`, `5.6.36-apache-stretch`, `5.6.37-apache-stretch`, `5.6.38-apache-stretch`, `5.6.39-apache-stretch`, `5.6.40-apache-stretch`, `7.0-apache-stretch`, `7.0.30-apache-stretch`, `7.0.31-apache-stretch`, `7.0.32-apache-stretch`, `7.0.33-apache-stretch`, `7.1-apache-stretch`, `7.1.17-apache-stretch`, `7.1.18-apache-stretch`, `7.1.19-apache-stretch`, `7.1.20-apache-stretch`, `7.1.21-apache-stretch`, `7.1.22-apache-stretch`, `7.1.23-apache-stretch`, `7.1.24-apache-stretch`, `7.1.25-apache-stretch`, `7.1.26-apache-stretch`, `7.1.27-apache-stretch`, `7.1.28-apache-stretch`, `7.1.29-apache-stretch`, `7.1.30-apache-stretch`, `7.1.31-apache-stretch`, `7.2-apache-stretch`, `7.2.0-apache-stretch`, `7.2.0RC4-apache-stretch`, `7.2.0RC5-apache-stretch`, `7.2.0RC6-apache-stretch`, `7.2.1-apache-stretch`, `7.2.10-apache-stretch`, `7.2.11-apache-stretch`, `7.2.12-apache-stretch`, `7.2.13-apache-stretch`, `7.2.14-apache-stretch`, `7.2.15-apache-stretch`, `7.2.16-apache-stretch`, `7.2.17-apache-stretch`, `7.2.18-apache-stretch`, `7.2.19-apache-stretch`, `7.2.2-apache-stretch`, `7.2.20-apache-stretch`, `7.2.21-apache-stretch`, `7.2.3-apache-stretch`, `7.2.4-apache-stretch`, `7.2.5-apache-stretch`, `7.2.6-apache-stretch`, `7.2.7-apache-stretch`, `7.2.8-apache-stretch`, `7.2.9-apache-stretch`, `7.2edge-apache-stretch`, `7.2unstable-apache-stretch`, `7.3-apache-stretch`, `7.3.0-apache-stretch`, `7.3.0RC1-apache-stretch`, `7.3.0RC2-apache-stretch`, `7.3.0RC3-apache-stretch`, `7.3.0RC4-apache-stretch`, `7.3.0RC5-apache-stretch`, `7.3.0RC6-apache-stretch`, `7.3.0beta2-apache-stretch`, `7.3.0beta3-apache-stretch`, `7.3.1-apache-stretch`, `7.3.2-apache-stretch`, `7.3.3-apache-stretch`, `7.3.4-apache-stretch`, `7.3.5-apache-stretch`, `7.3.6-apache-stretch`, `7.3.7-apache-stretch`, `7.3.8-apache-stretch`, `7.3edge-apache-stretch`, `7.3unstable-apache-stretch`, `7.4.0alpha1-apache-stretch`, `7.4.0alpha2-apache-stretch`, `7.4edge-apache-stretch`, `7.4unstable-apache-stretch`, `edge-apache-stretch`, `latest-apache-stretch`
  * cli-stretch branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.cli-stretch): `5.6-cli-stretch`, `5.6.36-cli-stretch`, `5.6.37-cli-stretch`, `5.6.38-cli-stretch`, `5.6.39-cli-stretch`, `5.6.40-cli-stretch`, `7.0-cli-stretch`, `7.0.30-cli-stretch`, `7.0.31-cli-stretch`, `7.0.32-cli-stretch`, `7.0.33-cli-stretch`, `7.1-cli-stretch`, `7.1.17-cli-stretch`, `7.1.18-cli-stretch`, `7.1.19-cli-stretch`, `7.1.20-cli-stretch`, `7.1.21-cli-stretch`, `7.1.22-cli-stretch`, `7.1.23-cli-stretch`, `7.1.24-cli-stretch`, `7.1.25-cli-stretch`, `7.1.26-cli-stretch`, `7.1.27-cli-stretch`, `7.1.28-cli-stretch`, `7.1.29-cli-stretch`, `7.1.30-cli-stretch`, `7.1.31-cli-stretch`, `7.2-cli-stretch`, `7.2.0-cli-stretch`, `7.2.0RC4-cli-stretch`, `7.2.0RC5-cli-stretch`, `7.2.0RC6-cli-stretch`, `7.2.1-cli-stretch`, `7.2.10-cli-stretch`, `7.2.11-cli-stretch`, `7.2.12-cli-stretch`, `7.2.13-cli-stretch`, `7.2.14-cli-stretch`, `7.2.15-cli-stretch`, `7.2.16-cli-stretch`, `7.2.17-cli-stretch`, `7.2.18-cli-stretch`, `7.2.19-cli-stretch`, `7.2.2-cli-stretch`, `7.2.20-cli-stretch`, `7.2.21-cli-stretch`, `7.2.3-cli-stretch`, `7.2.4-cli-stretch`, `7.2.5-cli-stretch`, `7.2.6-cli-stretch`, `7.2.7-cli-stretch`, `7.2.8-cli-stretch`, `7.2.9-cli-stretch`, `7.2edge-cli-stretch`, `7.2unstable-cli-stretch`, `7.3-cli-stretch`, `7.3.0-cli-stretch`, `7.3.0RC1-cli-stretch`, `7.3.0RC2-cli-stretch`, `7.3.0RC3-cli-stretch`, `7.3.0RC4-cli-stretch`, `7.3.0RC5-cli-stretch`, `7.3.0RC6-cli-stretch`, `7.3.0beta2-cli-stretch`, `7.3.0beta3-cli-stretch`, `7.3.1-cli-stretch`, `7.3.2-cli-stretch`, `7.3.3-cli-stretch`, `7.3.4-cli-stretch`, `7.3.5-cli-stretch`, `7.3.6-cli-stretch`, `7.3.7-cli-stretch`, `7.3.8-cli-stretch`, `7.3edge-cli-stretch`, `7.3unstable-cli-stretch`, `7.4.0alpha1-cli-stretch`, `7.4.0alpha2-cli-stretch`, `7.4edge-cli-stretch`, `7.4unstable-cli-stretch`, `edge-cli-stretch`, `latest-cli-stretch`
  * fpm-buster branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.fpm-buster): 
  * apache-buster branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.apache-buster): 
  * cli-buster branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.cli-buster): 
  * fpm-alpine branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.fpm-alpine): `5.5-fpm-alpine`, `5.5.33-fpm-alpine`, `5.5.34-fpm-alpine`, `5.5.35-fpm-alpine`, `5.5.36-fpm-alpine`, `5.5.37-fpm-alpine`, `5.5.38-fpm-alpine`, `5.6-fpm-alpine`, `5.6.19-fpm-alpine`, `5.6.20-fpm-alpine`, `5.6.21-fpm-alpine`, `5.6.22-fpm-alpine`, `5.6.23-fpm-alpine`, `5.6.24-fpm-alpine`, `5.6.25-fpm-alpine`, `5.6.26-fpm-alpine`, `5.6.27-fpm-alpine`, `5.6.28-fpm-alpine`, `5.6.29-fpm-alpine`, `5.6.30-fpm-alpine`, `5.6.31-fpm-alpine`, `5.6.32-fpm-alpine`, `5.6.33-fpm-alpine`, `5.6.34-fpm-alpine`, `5.6.35-fpm-alpine`, `5.6.36-fpm-alpine`, `5.6.37-fpm-alpine`, `5.6.38-fpm-alpine`, `5.6.39-fpm-alpine`, `5.6.40-fpm-alpine`, `7.0-fpm-alpine`, `7.0.10-fpm-alpine`, `7.0.11-fpm-alpine`, `7.0.12-fpm-alpine`, `7.0.13-fpm-alpine`, `7.0.14-fpm-alpine`, `7.0.15-fpm-alpine`, `7.0.16-fpm-alpine`, `7.0.17-fpm-alpine`, `7.0.18-fpm-alpine`, `7.0.19-fpm-alpine`, `7.0.20-fpm-alpine`, `7.0.21-fpm-alpine`, `7.0.22-fpm-alpine`, `7.0.23-fpm-alpine`, `7.0.24-fpm-alpine`, `7.0.25-fpm-alpine`, `7.0.26-fpm-alpine`, `7.0.27-fpm-alpine`, `7.0.28-fpm-alpine`, `7.0.29-fpm-alpine`, `7.0.30-fpm-alpine`, `7.0.31-fpm-alpine`, `7.0.32-fpm-alpine`, `7.0.33-fpm-alpine`, `7.0.4-fpm-alpine`, `7.0.5-fpm-alpine`, `7.0.6-fpm-alpine`, `7.0.7-fpm-alpine`, `7.0.8-fpm-alpine`, `7.0.9-fpm-alpine`, `7.1-fpm-alpine`, `7.1.0-fpm-alpine`, `7.1.0RC1-fpm-alpine`, `7.1.0RC2-fpm-alpine`, `7.1.0RC3-fpm-alpine`, `7.1.0RC4-fpm-alpine`, `7.1.0RC5-fpm-alpine`, `7.1.0RC6-fpm-alpine`, `7.1.1-fpm-alpine`, `7.1.10-fpm-alpine`, `7.1.11-fpm-alpine`, `7.1.12-fpm-alpine`, `7.1.13-fpm-alpine`, `7.1.14-fpm-alpine`, `7.1.15-fpm-alpine`, `7.1.16-fpm-alpine`, `7.1.17-fpm-alpine`, `7.1.18-fpm-alpine`, `7.1.19-fpm-alpine`, `7.1.2-fpm-alpine`, `7.1.20-fpm-alpine`, `7.1.21-fpm-alpine`, `7.1.22-fpm-alpine`, `7.1.23-fpm-alpine`, `7.1.24-fpm-alpine`, `7.1.25-fpm-alpine`, `7.1.26-fpm-alpine`, `7.1.27-fpm-alpine`, `7.1.28-fpm-alpine`, `7.1.29-fpm-alpine`, `7.1.3-fpm-alpine`, `7.1.30-fpm-alpine`, `7.1.31-fpm-alpine`, `7.1.4-fpm-alpine`, `7.1.5-fpm-alpine`, `7.1.6-fpm-alpine`, `7.1.7-fpm-alpine`, `7.1.8-fpm-alpine`, `7.1.9-fpm-alpine`, `7.2-fpm-alpine`, `7.2.0-fpm-alpine`, `7.2.0RC1-fpm-alpine`, `7.2.0RC2-fpm-alpine`, `7.2.0RC3-fpm-alpine`, `7.2.0RC4-fpm-alpine`, `7.2.0RC5-fpm-alpine`, `7.2.0RC6-fpm-alpine`, `7.2.0alpha3-fpm-alpine`, `7.2.0beta1-fpm-alpine`, `7.2.0beta2-fpm-alpine`, `7.2.0beta3-fpm-alpine`, `7.2.1-fpm-alpine`, `7.2.10-fpm-alpine`, `7.2.11-fpm-alpine`, `7.2.12-fpm-alpine`, `7.2.13-fpm-alpine`, `7.2.14-fpm-alpine`, `7.2.15-fpm-alpine`, `7.2.16-fpm-alpine`, `7.2.17-fpm-alpine`, `7.2.18-fpm-alpine`, `7.2.19-fpm-alpine`, `7.2.2-fpm-alpine`, `7.2.20-fpm-alpine`, `7.2.21-fpm-alpine`, `7.2.3-fpm-alpine`, `7.2.4-fpm-alpine`, `7.2.5-fpm-alpine`, `7.2.6-fpm-alpine`, `7.2.7-fpm-alpine`, `7.2.8-fpm-alpine`, `7.2.9-fpm-alpine`, `7.2edge-fpm-alpine`, `7.2unstable-fpm-alpine`, `7.3-fpm-alpine`, `7.3.0-fpm-alpine`, `7.3.0RC1-fpm-alpine`, `7.3.0RC2-fpm-alpine`, `7.3.0RC3-fpm-alpine`, `7.3.0RC4-fpm-alpine`, `7.3.0RC5-fpm-alpine`, `7.3.0RC6-fpm-alpine`, `7.3.0beta2-fpm-alpine`, `7.3.0beta3-fpm-alpine`, `7.3.1-fpm-alpine`, `7.3.2-fpm-alpine`, `7.3.3-fpm-alpine`, `7.3.4-fpm-alpine`, `7.3.5-fpm-alpine`, `7.3.6-fpm-alpine`, `7.3.7-fpm-alpine`, `7.3.8-fpm-alpine`, `7.3edge-fpm-alpine`, `7.3unstable-fpm-alpine`, `7.4.0alpha1-fpm-alpine`, `7.4.0alpha2-fpm-alpine`, `7.4.0alpha3-fpm-alpine`, `7.4.0beta1-fpm-alpine`, `7.4edge-fpm-alpine`, `7.4unstable-fpm-alpine`, `edge-fpm-alpine`, `latest-fpm-alpine`
  * cli-alpine branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.cli-alpine): `5.6-cli-alpine`, `5.6.31-cli-alpine`, `5.6.32-cli-alpine`, `5.6.33-cli-alpine`, `5.6.34-cli-alpine`, `5.6.35-cli-alpine`, `5.6.36-cli-alpine`, `5.6.37-cli-alpine`, `5.6.38-cli-alpine`, `5.6.39-cli-alpine`, `5.6.40-cli-alpine`, `7.0-cli-alpine`, `7.0.24-cli-alpine`, `7.0.25-cli-alpine`, `7.0.26-cli-alpine`, `7.0.27-cli-alpine`, `7.0.28-cli-alpine`, `7.0.29-cli-alpine`, `7.0.30-cli-alpine`, `7.0.31-cli-alpine`, `7.0.32-cli-alpine`, `7.0.33-cli-alpine`, `7.1-cli-alpine`, `7.1.10-cli-alpine`, `7.1.11-cli-alpine`, `7.1.12-cli-alpine`, `7.1.13-cli-alpine`, `7.1.14-cli-alpine`, `7.1.15-cli-alpine`, `7.1.16-cli-alpine`, `7.1.17-cli-alpine`, `7.1.18-cli-alpine`, `7.1.19-cli-alpine`, `7.1.20-cli-alpine`, `7.1.21-cli-alpine`, `7.1.22-cli-alpine`, `7.1.23-cli-alpine`, `7.1.24-cli-alpine`, `7.1.25-cli-alpine`, `7.1.26-cli-alpine`, `7.1.27-cli-alpine`, `7.1.28-cli-alpine`, `7.1.29-cli-alpine`, `7.1.30-cli-alpine`, `7.1.31-cli-alpine`, `7.2-cli-alpine`, `7.2.0-cli-alpine`, `7.2.0RC4-cli-alpine`, `7.2.0RC5-cli-alpine`, `7.2.0RC6-cli-alpine`, `7.2.1-cli-alpine`, `7.2.10-cli-alpine`, `7.2.11-cli-alpine`, `7.2.12-cli-alpine`, `7.2.13-cli-alpine`, `7.2.14-cli-alpine`, `7.2.15-cli-alpine`, `7.2.16-cli-alpine`, `7.2.17-cli-alpine`, `7.2.18-cli-alpine`, `7.2.19-cli-alpine`, `7.2.2-cli-alpine`, `7.2.20-cli-alpine`, `7.2.21-cli-alpine`, `7.2.3-cli-alpine`, `7.2.4-cli-alpine`, `7.2.5-cli-alpine`, `7.2.6-cli-alpine`, `7.2.7-cli-alpine`, `7.2.8-cli-alpine`, `7.2.9-cli-alpine`, `7.2edge-cli-alpine`, `7.2unstable-cli-alpine`, `7.3-cli-alpine`, `7.3.0-cli-alpine`, `7.3.0RC1-cli-alpine`, `7.3.0RC2-cli-alpine`, `7.3.0RC3-cli-alpine`, `7.3.0RC4-cli-alpine`, `7.3.0RC5-cli-alpine`, `7.3.0RC6-cli-alpine`, `7.3.0beta2-cli-alpine`, `7.3.0beta3-cli-alpine`, `7.3.1-cli-alpine`, `7.3.2-cli-alpine`, `7.3.3-cli-alpine`, `7.3.4-cli-alpine`, `7.3.5-cli-alpine`, `7.3.6-cli-alpine`, `7.3.7-cli-alpine`, `7.3.8-cli-alpine`, `7.3edge-cli-alpine`, `7.3unstable-cli-alpine`, `7.4.0alpha1-cli-alpine`, `7.4.0alpha2-cli-alpine`, `7.4.0alpha3-cli-alpine`, `7.4.0beta1-cli-alpine`, `7.4edge-cli-alpine`, `7.4unstable-cli-alpine`, `edge-cli-alpine`, `latest-cli-alpine`
  * fpm-alpine3.6 branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.fpm-alpine): `7.2-fpm-alpine3.6`, `7.2.0-fpm-alpine3.6`, `7.2.0RC4-fpm-alpine3.6`, `7.2.0RC5-fpm-alpine3.6`, `7.2.0RC6-fpm-alpine3.6`, `7.2.1-fpm-alpine3.6`, `7.2.10-fpm-alpine3.6`, `7.2.11-fpm-alpine3.6`, `7.2.2-fpm-alpine3.6`, `7.2.3-fpm-alpine3.6`, `7.2.4-fpm-alpine3.6`, `7.2.5-fpm-alpine3.6`, `7.2.6-fpm-alpine3.6`, `7.2.7-fpm-alpine3.6`, `7.2.8-fpm-alpine3.6`, `7.2.9-fpm-alpine3.6`, `7.2edge-fpm-alpine3.6`, `7.2unstable-fpm-alpine3.6`, `edge-fpm-alpine3.6`, `latest-fpm-alpine3.6`
  * cli-alpine3.6 branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.cli-alpine): `7.2-cli-alpine3.6`, `7.2.0-cli-alpine3.6`, `7.2.0RC4-cli-alpine3.6`, `7.2.0RC5-cli-alpine3.6`, `7.2.0RC6-cli-alpine3.6`, `7.2.1-cli-alpine3.6`, `7.2.10-cli-alpine3.6`, `7.2.11-cli-alpine3.6`, `7.2.2-cli-alpine3.6`, `7.2.3-cli-alpine3.6`, `7.2.4-cli-alpine3.6`, `7.2.5-cli-alpine3.6`, `7.2.6-cli-alpine3.6`, `7.2.7-cli-alpine3.6`, `7.2.8-cli-alpine3.6`, `7.2.9-cli-alpine3.6`, `7.2edge-cli-alpine3.6`, `7.2unstable-cli-alpine3.6`, `edge-cli-alpine3.6`, `latest-cli-alpine3.6`
  * fpm-alpine3.7 branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.fpm-alpine): `5.6-fpm-alpine3.7`, `5.6.36-fpm-alpine3.7`, `5.6.37-fpm-alpine3.7`, `5.6.38-fpm-alpine3.7`, `7.0-fpm-alpine3.7`, `7.0.30-fpm-alpine3.7`, `7.0.31-fpm-alpine3.7`, `7.0.32-fpm-alpine3.7`, `7.0.33-fpm-alpine3.7`, `7.1-fpm-alpine3.7`, `7.1.17-fpm-alpine3.7`, `7.1.18-fpm-alpine3.7`, `7.1.19-fpm-alpine3.7`, `7.1.20-fpm-alpine3.7`, `7.1.21-fpm-alpine3.7`, `7.1.22-fpm-alpine3.7`, `7.1.23-fpm-alpine3.7`, `7.2-fpm-alpine3.7`, `7.2.0-fpm-alpine3.7`, `7.2.1-fpm-alpine3.7`, `7.2.10-fpm-alpine3.7`, `7.2.11-fpm-alpine3.7`, `7.2.2-fpm-alpine3.7`, `7.2.3-fpm-alpine3.7`, `7.2.4-fpm-alpine3.7`, `7.2.5-fpm-alpine3.7`, `7.2.6-fpm-alpine3.7`, `7.2.7-fpm-alpine3.7`, `7.2.8-fpm-alpine3.7`, `7.2.9-fpm-alpine3.7`, `7.2edge-fpm-alpine3.7`, `edge-fpm-alpine3.7`, `latest-fpm-alpine3.7`
  * cli-alpine3.7 branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.cli-alpine): `5.6-cli-alpine3.7`, `5.6.36-cli-alpine3.7`, `5.6.37-cli-alpine3.7`, `5.6.38-cli-alpine3.7`, `7.0-cli-alpine3.7`, `7.0.30-cli-alpine3.7`, `7.0.31-cli-alpine3.7`, `7.0.32-cli-alpine3.7`, `7.0.33-cli-alpine3.7`, `7.1-cli-alpine3.7`, `7.1.17-cli-alpine3.7`, `7.1.18-cli-alpine3.7`, `7.1.19-cli-alpine3.7`, `7.1.20-cli-alpine3.7`, `7.1.21-cli-alpine3.7`, `7.1.22-cli-alpine3.7`, `7.1.23-cli-alpine3.7`, `7.2-cli-alpine3.7`, `7.2.0-cli-alpine3.7`, `7.2.1-cli-alpine3.7`, `7.2.10-cli-alpine3.7`, `7.2.11-cli-alpine3.7`, `7.2.2-cli-alpine3.7`, `7.2.3-cli-alpine3.7`, `7.2.4-cli-alpine3.7`, `7.2.5-cli-alpine3.7`, `7.2.6-cli-alpine3.7`, `7.2.7-cli-alpine3.7`, `7.2.8-cli-alpine3.7`, `7.2.9-cli-alpine3.7`, `7.2edge-cli-alpine3.7`, `edge-cli-alpine3.7`, `latest-cli-alpine3.7`
  * fpm-alpine3.8 branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.fpm-alpine): `5.6-fpm-alpine3.8`, `5.6.37-fpm-alpine3.8`, `5.6.38-fpm-alpine3.8`, `5.6.39-fpm-alpine3.8`, `5.6.40-fpm-alpine3.8`, `7.1-fpm-alpine3.8`, `7.1.21-fpm-alpine3.8`, `7.1.22-fpm-alpine3.8`, `7.1.23-fpm-alpine3.8`, `7.1.24-fpm-alpine3.8`, `7.1.25-fpm-alpine3.8`, `7.1.26-fpm-alpine3.8`, `7.1.27-fpm-alpine3.8`, `7.1.28-fpm-alpine3.8`, `7.1.29-fpm-alpine3.8`, `7.1.30-fpm-alpine3.8`, `7.2-fpm-alpine3.8`, `7.2.10-fpm-alpine3.8`, `7.2.11-fpm-alpine3.8`, `7.2.12-fpm-alpine3.8`, `7.2.13-fpm-alpine3.8`, `7.2.14-fpm-alpine3.8`, `7.2.15-fpm-alpine3.8`, `7.2.16-fpm-alpine3.8`, `7.2.17-fpm-alpine3.8`, `7.2.18-fpm-alpine3.8`, `7.2.19-fpm-alpine3.8`, `7.2.9-fpm-alpine3.8`, `7.2edge-fpm-alpine3.8`, `7.3-fpm-alpine3.8`, `7.3.0-fpm-alpine3.8`, `7.3.0RC1-fpm-alpine3.8`, `7.3.0RC2-fpm-alpine3.8`, `7.3.0RC3-fpm-alpine3.8`, `7.3.0RC4-fpm-alpine3.8`, `7.3.0RC5-fpm-alpine3.8`, `7.3.0RC6-fpm-alpine3.8`, `7.3.0beta2-fpm-alpine3.8`, `7.3.0beta3-fpm-alpine3.8`, `7.3.1-fpm-alpine3.8`, `7.3.2-fpm-alpine3.8`, `7.3.3-fpm-alpine3.8`, `7.3.4-fpm-alpine3.8`, `7.3.5-fpm-alpine3.8`, `7.3.6-fpm-alpine3.8`, `7.3edge-fpm-alpine3.8`, `7.3unstable-fpm-alpine3.8`, `edge-fpm-alpine3.8`, `latest-fpm-alpine3.8`
  * cli-alpine3.8 branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.cli-alpine): `5.6-cli-alpine3.8`, `5.6.37-cli-alpine3.8`, `5.6.38-cli-alpine3.8`, `5.6.39-cli-alpine3.8`, `5.6.40-cli-alpine3.8`, `7.1-cli-alpine3.8`, `7.1.21-cli-alpine3.8`, `7.1.22-cli-alpine3.8`, `7.1.23-cli-alpine3.8`, `7.1.24-cli-alpine3.8`, `7.1.25-cli-alpine3.8`, `7.1.26-cli-alpine3.8`, `7.1.27-cli-alpine3.8`, `7.1.28-cli-alpine3.8`, `7.1.29-cli-alpine3.8`, `7.1.30-cli-alpine3.8`, `7.2-cli-alpine3.8`, `7.2.10-cli-alpine3.8`, `7.2.11-cli-alpine3.8`, `7.2.12-cli-alpine3.8`, `7.2.13-cli-alpine3.8`, `7.2.14-cli-alpine3.8`, `7.2.15-cli-alpine3.8`, `7.2.16-cli-alpine3.8`, `7.2.17-cli-alpine3.8`, `7.2.18-cli-alpine3.8`, `7.2.19-cli-alpine3.8`, `7.2.9-cli-alpine3.8`, `7.2edge-cli-alpine3.8`, `7.3-cli-alpine3.8`, `7.3.0-cli-alpine3.8`, `7.3.0RC1-cli-alpine3.8`, `7.3.0RC2-cli-alpine3.8`, `7.3.0RC3-cli-alpine3.8`, `7.3.0RC4-cli-alpine3.8`, `7.3.0RC5-cli-alpine3.8`, `7.3.0RC6-cli-alpine3.8`, `7.3.0beta2-cli-alpine3.8`, `7.3.0beta3-cli-alpine3.8`, `7.3.1-cli-alpine3.8`, `7.3.2-cli-alpine3.8`, `7.3.3-cli-alpine3.8`, `7.3.4-cli-alpine3.8`, `7.3.5-cli-alpine3.8`, `7.3.6-cli-alpine3.8`, `7.3edge-cli-alpine3.8`, `7.3unstable-cli-alpine3.8`, `edge-cli-alpine3.8`, `latest-cli-alpine3.8`
  * fpm-alpine3.9 branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.fpm-alpine): `7.1-fpm-alpine3.9`, `7.1.26-fpm-alpine3.9`, `7.1.27-fpm-alpine3.9`, `7.1.28-fpm-alpine3.9`, `7.1.29-fpm-alpine3.9`, `7.1.30-fpm-alpine3.9`, `7.1.31-fpm-alpine3.9`, `7.2-fpm-alpine3.9`, `7.2.14-fpm-alpine3.9`, `7.2.15-fpm-alpine3.9`, `7.2.16-fpm-alpine3.9`, `7.2.17-fpm-alpine3.9`, `7.2.18-fpm-alpine3.9`, `7.2.19-fpm-alpine3.9`, `7.2.20-fpm-alpine3.9`, `7.2.21-fpm-alpine3.9`, `7.3-fpm-alpine3.9`, `7.3.1-fpm-alpine3.9`, `7.3.2-fpm-alpine3.9`, `7.3.3-fpm-alpine3.9`, `7.3.4-fpm-alpine3.9`, `7.3.5-fpm-alpine3.9`, `7.3.6-fpm-alpine3.9`, `7.3.7-fpm-alpine3.9`, `7.3.8-fpm-alpine3.9`, `7.3edge-fpm-alpine3.9`, `7.4.0alpha1-fpm-alpine3.9`, `7.4.0alpha2-fpm-alpine3.9`, `7.4edge-fpm-alpine3.9`, `7.4unstable-fpm-alpine3.9`, `edge-fpm-alpine3.9`, `latest-fpm-alpine3.9`
  * cli-alpine3.9 branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.cli-alpine): `7.1-cli-alpine3.9`, `7.1.26-cli-alpine3.9`, `7.1.27-cli-alpine3.9`, `7.1.28-cli-alpine3.9`, `7.1.29-cli-alpine3.9`, `7.1.30-cli-alpine3.9`, `7.1.31-cli-alpine3.9`, `7.2-cli-alpine3.9`, `7.2.14-cli-alpine3.9`, `7.2.15-cli-alpine3.9`, `7.2.16-cli-alpine3.9`, `7.2.17-cli-alpine3.9`, `7.2.18-cli-alpine3.9`, `7.2.19-cli-alpine3.9`, `7.2.20-cli-alpine3.9`, `7.2.21-cli-alpine3.9`, `7.3-cli-alpine3.9`, `7.3.1-cli-alpine3.9`, `7.3.2-cli-alpine3.9`, `7.3.3-cli-alpine3.9`, `7.3.4-cli-alpine3.9`, `7.3.5-cli-alpine3.9`, `7.3.6-cli-alpine3.9`, `7.3.8-cli-alpine3.9`, `7.3edge-cli-alpine3.9`, `7.4.0alpha1-cli-alpine3.9`, `7.4.0alpha2-cli-alpine3.9`, `7.4edge-cli-alpine3.9`, `7.4unstable-cli-alpine3.9`, `edge-cli-alpine3.9`, `latest-cli-alpine3.9`
  * fpm-alpine3.10 branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.fpm-alpine): `7.1-fpm-alpine3.10`, `7.1.30-fpm-alpine3.10`, `7.1.31-fpm-alpine3.10`, `7.2-fpm-alpine3.10`, `7.2.19-fpm-alpine3.10`, `7.2.20-fpm-alpine3.10`, `7.2.21-fpm-alpine3.10`, `7.3-fpm-alpine3.10`, `7.3.6-fpm-alpine3.10`, `7.3.7-fpm-alpine3.10`, `7.3.8-fpm-alpine3.10`, `7.3edge-fpm-alpine3.10`, `7.4.0alpha2-fpm-alpine3.10`, `7.4.0alpha3-fpm-alpine3.10`, `7.4.0beta1-fpm-alpine3.10`, `7.4edge-fpm-alpine3.10`, `7.4unstable-fpm-alpine3.10`, `edge-fpm-alpine3.10`, `latest-fpm-alpine3.10`
  * cli-alpine3.10 branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/Dockerfile.cli-alpine): `7.1-cli-alpine3.10`, `7.1.30-cli-alpine3.10`, `7.1.31-cli-alpine3.10`, `7.2-cli-alpine3.10`, `7.2.19-cli-alpine3.10`, `7.2.20-cli-alpine3.10`, `7.2.21-cli-alpine3.10`, `7.3-cli-alpine3.10`, `7.3.6-cli-alpine3.10`, `7.3.7-cli-alpine3.10`, `7.3.8-cli-alpine3.10`, `7.3edge-cli-alpine3.10`, `7.4.0alpha2-cli-alpine3.10`, `7.4.0alpha3-cli-alpine3.10`, `7.4.0beta1-cli-alpine3.10`, `7.4edge-cli-alpine3.10`, `7.4unstable-cli-alpine3.10`, `edge-cli-alpine3.10`, `latest-cli-alpine3.10`

<!--- END_TAGS_LIST -->
