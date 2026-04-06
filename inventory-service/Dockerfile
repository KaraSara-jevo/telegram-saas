FROM php:8.2-fpm

ENV COMPOSER_IPRESOLVE=4

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip

# Clear cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install PHP extensions
RUN docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd

# Get latest Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www

COPY . /var/www

RUN composer config -g secure-http false \
    && composer config -g repo.packagist composer http://mirrors.aliyun.com/composer/ \
    && composer install --no-interaction --prefer-dist --optimize-autoloader --no-progress --no-scripts

RUN chown -R www-data:www-data /var/www
