(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['jquery'], factory);
    } else {
        // Browser globals
        factory(root.jQuery);
    }
}(typeof self !== 'undefined' ? self : this, function ($) {
  $(function() {
    // Open FAQ Block when location hash is set
    if (window.location.hash) {
      jQuery(window.location.hash + '~ .sl-block-content .faqblock > input').attr('checked', true)
    }
  });
}));
