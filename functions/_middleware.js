// 旧ドメイン(tomo-architect.com)へのアクセスを新ドメインへ301転送する
const OLD_HOSTS = ['tomo-architect.com', 'www.tomo-architect.com'];
const NEW_ORIGIN = 'https://uyama-architecture.com';

export function onRequest(context) {
  const url = new URL(context.request.url);
  if (OLD_HOSTS.includes(url.hostname)) {
    return Response.redirect(NEW_ORIGIN + url.pathname + url.search, 301);
  }
  return context.next();
}
