#-- *coding: utf8*--
import re


ADA_SYSTEM_DEFINED = 'ADA_SYSTEM_DEFINED'

def find_name(name, ctx, itype='var'):
    #print(ctx.types)
    name = name.upper()
    if itype == 'var':
        check_info = ctx.vars
    else:
        check_info = ctx.types
    direct_packages = [ctx.cur_spec.package, ADA_SYSTEM_DEFINED]
    direct_packages.extend(ctx.cur_spec.use_list)
    for pakcage in direct_packages:
        if pakcage in check_info:
            if name in check_info[pakcage]:
                return check_info[pakcage][name], True
    idents = name.split('.')
    if len(idents) > 1:
        for i in range(1, len(idents)):
            pakcage = ".".join(idents[:i])
            t_name = ".".join(idents[i:])
            if pakcage in check_info and pakcage in ctx.cur_spec.with_list:
                if t_name in check_info[pakcage]:
                    return check_info[pakcage][t_name], True
    return name, False

def check_solved(ctx, name, solved):
    pass

def solve_type(ctx, i_type):
    return find_name(i_type, ctx, 'type')

def solve_expr(ctx, i_expr):
    res = re.findall("[a-zA-Z]\w*(?:[.'][a-zA-Z]\w*)*", i_expr)
    res = set(res)
    for name in res:
        has_attr =  "'" in name
        attr = ""
        if has_attr:
            attr = name[name.find("'")+1:]
            name = name[:name.find("'")]
        var, found = find_name(name, ctx, 'var')
        if found and not has_attr:
            if var.value_solved:
                i_expr = i_expr.replace(name, var.value)
        else:
            if found:
                var = var.data_type
            else:
                var, found = find_name(name, ctx, 'type')
            if found:
                attr2 = attr.lower()
                attr_v = getattr(var, attr2, None)
                if attr_v:
                    i_expr = i_expr.replace("'".join([name, attr]), attr_v)

    i_expr = re.sub('(\d)_(\d)', '\\1\\2', i_expr)
    i_expr = re.sub('(\d+)#(\d+)#', lambda x: str(int(x.group(2), int(x.group(1)))), i_expr)
    try:
        i_expr = str(eval(i_expr))
    except (NameError, SyntaxError) as ne:
        print('No solved: %s\n[%s]' % (ne, i_expr))
        return i_expr, False
    return i_expr, True

def get_texts(ctxs):
    if isinstance(ctxs, (list, set, tuple)):
        return list(map(lambda x: x.getText(), list(ctxs)))
    elif ctxs:
        return ctxs.getText()
    return None