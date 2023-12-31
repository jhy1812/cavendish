package com.windows33.cavendish.global.config;

import com.windows33.cavendish.domain.member.repository.MemberRepository;
import com.windows33.cavendish.domain.member.service.MemberService;
import com.windows33.cavendish.global.filter.ExceptionHandlerFilter;
import com.windows33.cavendish.global.jwt.JwtAuthenticationFilter;
import com.windows33.cavendish.global.jwt.JwtTokenProvider;
import com.windows33.cavendish.global.redis.RefreshTokenService;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import java.util.List;

@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtTokenProvider jwtTokenProvider;
    private final RefreshTokenService refreshTokenService;
    private final MemberRepository memberRepository;
    private final MemberService memberService;
    private final CorsConfig corsConfig;

    private static final String[] PERMIT_ALL = {
            /* swagger */
            "/api-docs/**",
            "/api/swagger-ui/**"
    };

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .httpBasic().disable()
                .csrf().disable()
                .cors().disable()
                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .and()
                .authorizeRequests()
                .antMatchers(PERMIT_ALL).permitAll()
                .antMatchers(HttpMethod.POST, "/api/member", "/api/member/**").permitAll()
                .antMatchers(HttpMethod.GET, "/api/board", "/api/board/**").permitAll()
                .antMatchers(HttpMethod.GET, "/api/image", "/api/image/**").permitAll()
                .antMatchers(HttpMethod.GET, "/api/comment", "/api/comment/**").permitAll()
                .antMatchers("/api/**").hasAuthority("USER")
                .anyRequest().authenticated()
                .and()
                .addFilterBefore(new JwtAuthenticationFilter(jwtTokenProvider, refreshTokenService, memberRepository, memberService), UsernamePasswordAuthenticationFilter.class)
                .addFilterBefore(new ExceptionHandlerFilter(), UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }

}